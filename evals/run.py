#!/usr/bin/env python3
"""Run design briefs through an agent CLI with these skills, then render the results for a person to judge.

  python3 evals/run.py run --runner codex --brief video-agent
  python3 evals/run.py run --runner claude --all
  python3 evals/run.py run --runner codex --all --dry-run
  python3 evals/run.py prompt --brief video-agent --dir /path/to/folder   print the prompt for any agent
  python3 evals/run.py check /path/to/folder --brief video-agent          check and render what it made
  python3 evals/run.py compare evals/out/<run>/<brief> evals/out/<run>/<brief> --blind

Taste is judged by a person looking at the sheet. The script checks only what a script can: that
the files exist, that the recorded deal is the one the script dealt, that each study carries the
brief's content, and that each one renders.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import random
import re
import shlex
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
SHOT = EVALS / "tools" / "shot.sh"
SKILL = ROOT / "skills" / "design-artifact-studio"
DIRECTIONS = (1, 2, 3)
SHEET_IMAGE_WIDTH = 760
FRAMED_BELOW = 500  # shot.sh frames narrower pages at the left of an image this wide


@dataclass(frozen=True)
class Brief:
    id: str
    title: str
    width: int
    height: int
    frame: str
    must_contain: tuple[str, ...]
    body: str


def parse_brief(text: str) -> Brief:
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    if not match:
        raise ValueError("no front matter")
    fields = dict(line.split(": ", 1) for line in match.group(1).splitlines() if ": " in line)
    missing = [key for key in ("id", "title", "width", "height", "frame", "must_contain") if key not in fields]
    if missing:
        raise ValueError("front matter lacks " + ", ".join(missing))
    return Brief(
        id=fields["id"].strip(),
        title=fields["title"].strip(),
        width=int(fields["width"]),
        height=int(fields["height"]),
        frame=fields["frame"].strip(),
        must_contain=tuple(part.strip() for part in fields["must_contain"].split("|") if part.strip()),
        body=match.group(2).strip(),
    )


def compose_prompt(brief: Brief, run_dir: Path) -> str:
    return f"""This is a delegated design task; proceed without a planning approval step.

First read the skill at {SKILL / "SKILL.md"} and follow it, including the reference files it tells you to read for this kind of work. Use only this copy: an older copy of the same skill may be installed on this machine, and it must not be read or followed. The skill folder is read-only for you: read it and run its script, but change nothing in it. If `python3` does not work in your shell, use {sys.executable}. Then complete the brief below according to that skill.

Brief:

{brief.body}

What I want now: the visual direction is open and I will choose it. Do not build a working prototype yet. Show me three distinct visual directions so I can pick one, with the same content and state in all three. You may search the web to look at how the products in this category present this screen.

Deliver, inside {run_dir}:
- direction-1.html, direction-2.html, direction-3.html: static studies of the deal's Directions 1, 2 and 3, for a {brief.width}px-wide window, each self-contained (embedded CSS; Google Fonts links allowed with a system-font fallback), no behavior needed. {brief.frame}
- renders/direction-1.png, direction-2.png, direction-3.png: final renders of each at {brief.width}x{brief.height}.
- deal.txt: what the skill's deal script printed, unedited. If you deal more than once, keep every output in order.
- DESIGN.md: the record the skill asks for, including the products you calibrated against and the three skeleton sketches.

Rendering. A renderer is available and is the only one you may use:
sh {SHOT} <absolute path to .html> <absolute path to out.png> [width] [height] [gray:]
It writes a PNG that you can open and look at, and can take up to a minute per image. Pass gray: after the height to render the page without color. Widths below {FRAMED_BELOW} are framed at the left of a {FRAMED_BELOW}px-wide image, with grey filling the rest. When you run the skill's likeness script on these renders, pass --width {brief.width}. Do not start servers or use any other browser, preview or screenshot tool.

Constraints: write only inside {run_dir}. Use fictional names only.

When done, reply with: the default you set aside, in one line; the products you calibrated against, and whether you inspected them or worked from memory; the seed; the cards you wrote and where each came from; then for each direction its name, whether it is the stretch, the values it was dealt, the card it carries, anything redrawn, and its gain and risk in one sentence."""


def runner_command(runner: str, prompt: str, run_dir: Path, sandbox: str, model: str | None) -> list[str]:
    if runner == "codex":
        # --search is a top-level flag: it lets the agent look at the category's products while calibrating
        command = ["codex", "--search", "exec", "--skip-git-repo-check", "-C", str(run_dir), "-s", sandbox,
                   "-o", str(run_dir / "_eval" / "last-message.txt")]
        return command + (["-m", model] if model else []) + [prompt]
    command = ["claude", "-p", prompt, "--output-format", "json", "--permission-mode", "acceptEdits",
               "--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "WebFetch",
               "--add-dir", str(ROOT)]
    return command + (["--model", model] if model else [])


# --- rendering on behalf of a sandboxed agent -------------------------------------------------

def inside(path: str, folder: Path) -> bool:
    try:
        Path(path).resolve().relative_to(folder.resolve())
    except ValueError:
        return False
    return True


def shot(src: Path | str, out: Path | str, width: int | str, height: int | str, steps: str = "") -> tuple[bool, str]:
    done = subprocess.run(["sh", str(SHOT), str(src), str(out), str(width), str(height), steps],
                          env={**os.environ, "SHOT_DIRECT": "1"}, capture_output=True, text=True)
    return done.returncode == 0, (done.stdout or done.stderr).strip()


def answer_render_request(request: Path, run_dir: Path) -> None:
    """A sandboxed agent cannot start Chrome; shot.sh leaves a request here and waits for the answer."""
    src, out, width, height, steps = (request.read_text(encoding="utf-8").split("\n") + [""] * 5)[:5]
    answer = request.with_suffix("")
    if inside(src, run_dir) and inside(out, run_dir):
        ok, message = shot(src, out, width, height, steps)
    else:
        ok, message = False, "render refused: the source and the output must be inside the run folder"
    Path(f"{answer}.ok" if ok else f"{answer}.err").write_text(message + "\n", encoding="utf-8")
    request.unlink()


def serve_render_queue(queue: Path, run_dir: Path, stop: threading.Event) -> None:
    while not stop.is_set():
        for request in sorted(queue.glob("*.req")):
            answer_render_request(request, run_dir)
        stop.wait(0.5)


# --- checks a script can make -----------------------------------------------------------------

def load_script(name: str):
    """One of the skill's scripts, loaded as a module without writing bytecode into the skill."""
    spec = importlib.util.spec_from_file_location(name, SKILL / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module


def load_deal():
    return load_script("draw_axes")


def check_deal(record: str, deal) -> tuple[bool, str]:
    """Every deal in deal.txt must be what the script prints for the seed and cards it names."""
    blocks = [block for block in re.split(r"(?m)^(?=seed \d+\s*$)", record) if "Direction 1" in block]
    if not blocks:
        return False, "no deal recorded"
    for block in blocks:
        lines = [line.rstrip() for line in block.strip().splitlines()]
        seed = int(lines[0].split()[1])
        deck = next((line.split(": ", 1)[1].strip() for line in lines if line.startswith("deck: ")), None)
        if deck not in getattr(deal, "DECKS", {}):
            return False, f"seed {seed}: no known deck recorded"
        usual = next((line.split(": ", 1)[1].strip() for line in lines if line.startswith("usual: ")), None)
        try:
            cards = [deal.parse_card(line[len("card: "):], deck) for line in lines if line.startswith("card: ")]
        except ValueError as error:
            return False, f"seed {seed}: {error}"
        expected = deal.describe(seed, cards, deck, usual).splitlines()
        if lines[: len(expected)] != expected:
            return False, (f"seed {seed}: the recorded sets are not what the script deals for that seed and those cards "
                           "(or draw_axes.py has changed since that deal)")
    last = blocks[-1].strip().splitlines()
    deck = next((l.split(": ", 1)[1].strip() for l in last if l.startswith("deck: ")), "?")
    return True, f"{len(blocks)} deal(s) reproduce; last is {last[0]}, {deck} deck, {sum(l.startswith('card: ') for l in last)} cards"


def last_deal(run_dir: Path) -> list[str]:
    record = run_dir / "deal.txt"
    """The last full deal in deal.txt; a single-axis redraw printed after it is not a deal."""
    blocks = re.split(r"(?m)^(?=seed \d+\s*$)", record.read_text(encoding="utf-8")) if record.is_file() else []
    deals = [block for block in blocks if "Direction 1" in block]
    return deals[-1].splitlines() if deals else []


def stretch_direction(run_dir: Path) -> int | None:
    """The direction the last deal marked as the stretch, if any."""
    found = [re.match(r"Direction (\d+) \(stretch\)", line) for line in last_deal(run_dir)]
    return next((int(match.group(1)) for match in found if match), None)


def listed_products(brief: Brief) -> list[str]:
    """Products the brief names on its "Products in this category:" line."""
    line = re.search(r"(?m)^Products in this category[^:]*:(.+)$", brief.body)
    if not line:
        return []
    names = re.split(r",|;|\band\b|\bor\b", re.sub(r"\([^)]*\)|such as", ",", line.group(1)))
    return [name.strip(" .") for name in names if name.strip(" .") and name.strip(" .")[0].isupper()]


def check_record(record: str, brief: Brief) -> tuple[bool, str]:
    """DESIGN.md names at least one of the products the brief lists, so calibration happened against them."""
    products = listed_products(brief)
    if not products:
        return True, "the brief lists no products"
    named = [product for product in products if product.casefold() in record.casefold()]
    return bool(named), ("names " + ", ".join(named)) if named else "names none of: " + ", ".join(products)


def plain(markup: str) -> str:
    text = html.unescape(re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", markup, flags=re.DOTALL | re.IGNORECASE))
    text = text.replace("’", "'").replace("‘", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", text).casefold()


def check_content(markup: str, must_contain: tuple[str, ...]) -> list[str]:
    text = plain(markup)
    return [needle for needle in must_contain if needle.casefold() not in text]


def check_self_contained(markup: str) -> list[str]:
    links = re.findall(r"<(?:script|img|link|iframe)\b[^>]*?(?:src|href)=[\"']([^\"']+)", markup, re.IGNORECASE)
    allowed = ("data:", "#", "https://fonts.googleapis.com", "https://fonts.gstatic.com")
    return [link for link in links if not link.startswith(allowed)]


def run_checks(brief: Brief, run_dir: Path) -> list[dict]:
    checks = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})

    wanted = [f"direction-{n}.html" for n in DIRECTIONS] + ["DESIGN.md", "deal.txt"]
    absent = [name for name in wanted if not (run_dir / name).is_file()]
    record("files", not absent, "all present" if not absent else "missing " + ", ".join(absent))

    deal_file = run_dir / "deal.txt"
    record("deal", *(check_deal(deal_file.read_text(encoding="utf-8"), load_deal()) if deal_file.is_file()
                     else (False, "no deal.txt")))
    design = run_dir / "DESIGN.md"
    if design.is_file():
        record("calibration", *check_record(design.read_text(encoding="utf-8", errors="replace"), brief))

    for n in DIRECTIONS:
        study = run_dir / f"direction-{n}.html"
        if not study.is_file():
            continue
        markup = study.read_text(encoding="utf-8", errors="replace")
        lacking = check_content(markup, brief.must_contain)
        record(f"content {n}", not lacking, "brief's content present" if not lacking else "missing: " + "; ".join(lacking))
        outside = check_self_contained(markup)
        record(f"self-contained {n}", not outside, "no outside files" if not outside else "loads " + ", ".join(outside[:3]))
        ok, message = shot(study, run_dir / "_eval" / f"direction-{n}.png", brief.width, brief.height)
        record(f"renders {n}", ok, message)
    renders = [run_dir / "_eval" / f"direction-{n}.png" for n in DIRECTIONS]
    if all(render.is_file() for render in renders):
        record("distinct", *check_distinct(renders, brief.width))
    return checks


def check_distinct(renders: list[Path], width: int) -> tuple[bool, str]:
    """No two studies read as one layout once color, tone and spacing are set aside: the skill's own test, rerun."""
    likeness = load_script("likeness")
    try:
        grids = [likeness.content_grid(render, width) for render in renders]
    except ValueError as error:
        return False, str(error)
    scores = {(i + 1, j + 1): likeness.likeness(grids[i], grids[j])
              for i in range(len(grids)) for j in range(i + 1, len(grids))}
    alike = [f"{a} and {b}" for (a, b), score in scores.items() if score >= likeness.ALIKE]
    shown = " · ".join(f"{a}–{b} {score:.2f}" for (a, b), score in scores.items())
    if alike:
        return False, f"{shown}; {', '.join(alike)} read as one layout (likeness {likeness.ALIKE} or more)"
    return True, f"{shown}; all below {likeness.ALIKE}"


# --- the sheet a person looks at --------------------------------------------------------------

def sheet_html(title: str, items: list[tuple[str, str, int]]) -> str:
    """items: (label, image path relative to the sheet, page width the image was rendered at)."""
    figures = []
    for label, image, width in items:
        shown = min(SHEET_IMAGE_WIDTH, width)
        full = max(width, FRAMED_BELOW)  # the PNG is wider than a narrow page; crop the frame away
        figures.append(
            f'<figure style="width:{shown}px"><figcaption>{html.escape(label)}</figcaption>'
            f'<div style="width:{shown}px;overflow:hidden"><img src="{html.escape(image)}" alt="" '
            f'style="width:{round(shown * full / width)}px"></div></figure>')
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>' + html.escape(title) + "</title><style>"
        'body{margin:0;background:#fff;color:#111;font:16px/1.3 -apple-system,"Helvetica Neue",Arial,sans-serif;padding:26px}'
        "h1{font-size:28px;margin:0 0 16px}.row{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}"
        "figure{margin:0}figcaption{font-weight:600;font-size:22px;margin:0 0 8px}"
        "img{display:block;border:1px solid #cfcfcf}"
        "</style></head><body><h1>" + html.escape(title) + '</h1><div class="row">' + "".join(figures) + "</div></body></html>")


def write_sheet(folder: Path, title: str, items: list[tuple[str, str, int]], height: int) -> tuple[bool, str]:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "sheet.html").write_text(sheet_html(title, items), encoding="utf-8")
    per_row = min(len(items), 3)
    shown = max(min(SHEET_IMAGE_WIDTH, width) for _, _, width in items)
    tallest = max(min(SHEET_IMAGE_WIDTH, width) * height / width for _, _, width in items)
    rows = -(-len(items) // per_row)
    return shot(folder / "sheet.html", folder / "sheet.png",
                per_row * shown + (per_row - 1) * 26 + 52, int(rows * (tallest + 60) + 100))


# --- commands ---------------------------------------------------------------------------------

def load_briefs(names: list[str], everything: bool) -> list[Brief]:
    paths = sorted((EVALS / "briefs").glob("*.md")) if everything else [EVALS / "briefs" / f"{name}.md" for name in names]
    briefs = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"no such brief: {path.stem}; available: " + ", ".join(p.stem for p in sorted((EVALS / 'briefs').glob('*.md'))))
        try:
            briefs.append(parse_brief(path.read_text(encoding="utf-8")))
        except ValueError as error:
            raise SystemExit(f"{path.relative_to(ROOT)}: {error}")
    return briefs


def usage_facts(runner: str, log: str) -> dict:
    """Model, tokens and cost as the CLI reports them; None where it reports nothing."""
    if runner == "codex":
        model = re.search(r"(?m)^model: (.+)$", log)
        tokens = re.search(r"tokens used\s*\n\s*([\d,]+)", log)
        return {"model": model.group(1).strip() if model else None,
                "tokens": int(tokens.group(1).replace(",", "")) if tokens else None}
    try:
        report = json.loads(log)
    except ValueError:
        return {"model": None}
    usage = report.get("usage") or {}
    return {"model": ", ".join(report.get("modelUsage") or {}) or None,
            "tokens": sum(usage.get(key) or 0 for key in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")) or None,
            "cost_usd": report.get("total_cost_usd"), "turns": report.get("num_turns"),
            "agent_error": report.get("is_error"), "permission_denials": len(report.get("permission_denials") or [])}


def final_reply(runner: str, log: str) -> str:
    if runner == "claude":
        try:
            return str(json.loads(log).get("result", ""))
        except ValueError:
            return log
    return log


def run_agent(command: list[str], run_dir: Path, log: Path, timeout: int, errors: Path | None = None) -> tuple[int | None, int]:
    stop = threading.Event()
    queue = run_dir / ".render-queue"
    queue.mkdir(exist_ok=True)
    worker = threading.Thread(target=serve_render_queue, args=(queue, run_dir, stop), daemon=True)
    worker.start()
    started = time.time()
    with log.open("w", encoding="utf-8") as output, (errors.open("w", encoding="utf-8") if errors else open(os.devnull, "w")) as error:
        process = subprocess.Popen(command, cwd=run_dir, stdin=subprocess.DEVNULL, stdout=output,
                                   stderr=error if errors else subprocess.STDOUT)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            code = None
    stop.set()
    worker.join(timeout=5)
    return code, int(time.time() - started)


def command_run(args: argparse.Namespace) -> int:
    briefs = load_briefs(args.brief, args.all)
    if not briefs:
        raise SystemExit("name a brief with --brief, or pass --all")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = Path(args.out).resolve() / "-".join(part for part in (stamp, args.runner, args.label) if part)
    failed = False
    for brief in briefs:
        run_dir = out / brief.id
        prompt = compose_prompt(brief, run_dir)
        command = runner_command(args.runner, prompt, run_dir, args.sandbox, args.model)
        if args.dry_run:
            shown = [part if part != prompt else f"<prompt, {len(prompt)} characters>" for part in command]
            print(f"{brief.id}: would run in {run_dir}\n  {' '.join(shlex.quote(part) for part in shown)}")
            continue
        (run_dir / "_eval").mkdir(parents=True, exist_ok=True)
        (run_dir / "_eval" / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
        log = run_dir / "_eval" / "agent.log"
        print(f"{brief.id}: running {args.runner} in {run_dir}", flush=True)
        # Claude's stdout is one JSON report; its warnings go to agent.err so they stay out of the reply
        errors = run_dir / "_eval" / "agent.err" if args.runner == "claude" else None
        code, seconds = run_agent(command, run_dir, log, args.timeout, errors)
        text = log.read_text(encoding="utf-8", errors="replace")
        if args.runner == "claude":
            (run_dir / "_eval" / "last-message.txt").write_text(final_reply("claude", text) + "\n", encoding="utf-8")
        if code != 0:
            tail = (errors.read_text(encoding="utf-8", errors="replace") if errors else "") + text
            print("  the agent did not finish cleanly; its output ends:\n    " + "\n    ".join(tail.strip().splitlines()[-4:]))
        facts = {"runner": args.runner, "exit": code, "seconds": seconds, "timed_out": code is None, **usage_facts(args.runner, text)}
        if args.model and not facts.get("model"):
            facts["model"] = args.model
        passed = assess(brief, run_dir, facts)
        failed = failed or code != 0 or not passed
    return 1 if failed else 0


def assess(brief: Brief, run_dir: Path, facts: dict) -> bool:
    """Check a finished folder, render its sheet, write result.json and report. True when every check passes."""
    (run_dir / "_eval").mkdir(parents=True, exist_ok=True)
    checks = run_checks(brief, run_dir)
    stretch = stretch_direction(run_dir)
    rendered = [(f"{brief.id} {n}" + (" · stretch" if n == stretch else ""), f"direction-{n}.png", brief.width)
                for n in DIRECTIONS if (run_dir / "_eval" / f"direction-{n}.png").is_file()]
    sheet = bool(rendered) and write_sheet(run_dir / "_eval", f"{brief.title} · {facts['runner']}", rendered, brief.height)[0]
    result = {"brief": brief.id, **facts, "checks": checks}
    (run_dir / "_eval" / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    passed = all(check["ok"] for check in checks)
    spent = ", ".join(part for part in (
        f"exit {facts['exit']}, {facts['seconds']}s" if "seconds" in facts else "",
        facts.get("model") or "",
        f"{facts['tokens']:,} tokens" if facts.get("tokens") else "",
        f"${facts['cost_usd']:.2f}" if facts.get("cost_usd") is not None else "") if part)
    print(f"{brief.id}: {'checks pass' if passed else 'CHECKS FAIL'}" + (f", {spent}" if spent else ""))
    for check in checks:
        if not check["ok"]:
            print(f"  {check['check']}: {check['detail']}")
    print(f"  sheet: {run_dir / '_eval' / 'sheet.png'}" if sheet else "  no sheet: nothing rendered")
    return passed


def command_prompt(args: argparse.Namespace) -> int:
    (brief,) = load_briefs([args.brief], False)
    print(compose_prompt(brief, Path(args.dir).resolve()))
    return 0


def command_check(args: argparse.Namespace) -> int:
    run_dir = Path(args.folder).resolve()
    (brief,) = load_briefs([args.brief or run_dir.name], False)
    return 0 if assess(brief, run_dir, {"runner": args.runner}) else 1


def command_compare(args: argparse.Namespace) -> int:
    entries = []
    for folder in (Path(path).resolve() for path in args.runs):
        result = json.loads((folder / "_eval" / "result.json").read_text(encoding="utf-8"))
        brief = parse_brief((EVALS / "briefs" / f"{result['brief']}.md").read_text(encoding="utf-8"))
        stretch = stretch_direction(folder)
        for n in DIRECTIONS:
            image = folder / "_eval" / f"direction-{n}.png"
            if image.is_file():
                entries.append((f"{folder.parent.name}/{folder.name} direction {n}" + (" · stretch" if n == stretch else ""), image, brief))
    if not entries:
        raise SystemExit("no rendered directions found in those folders")
    out = Path(args.out).resolve() / ("compare-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    out.mkdir(parents=True)
    if args.blind:
        random.shuffle(entries)
    items, mapping = [], []
    for index, (source, image, brief) in enumerate(entries):
        label = (chr(ord("A") + index) + (" · stretch" if source.endswith(" · stretch") else "")) if args.blind else source
        copy = out / f"{label.replace(' · ', '-').replace('/', '_').replace(' ', '-')}.png"
        copy.write_bytes(image.read_bytes())
        items.append((label, copy.name, brief.width))
        mapping.append(f"{label} = {source}")
    if args.blind:
        (out / "mapping.txt").write_text("\n".join(mapping) + "\n", encoding="utf-8")
    ok, message = write_sheet(out, "Compare" + (" (blind)" if args.blind else ""), items, max(e[2].height for e in entries))
    print(f"sheet: {out / 'sheet.png'}" if ok else message)
    if args.blind:
        print(f"mapping sealed in {out / 'mapping.txt'}; open it after judging")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="run briefs through an agent CLI and render the results")
    run.add_argument("--runner", choices=("codex", "claude"), required=True)
    run.add_argument("--brief", action="append", default=[], help="brief id under evals/briefs; repeatable")
    run.add_argument("--all", action="store_true", help="run every brief")
    run.add_argument("--model", help="model to ask the CLI for; default is the CLI's own")
    run.add_argument("--sandbox", default="workspace-write", help="codex sandbox mode (default: workspace-write)")
    run.add_argument("--timeout", type=int, default=3600, help="seconds allowed per brief (default: 3600)")
    run.add_argument("--label", default="", help="suffix for the run folder's name")
    run.add_argument("--out", default=str(EVALS / "out"))
    run.add_argument("--dry-run", action="store_true", help="print what would run and stop")
    run.set_defaults(handler=command_run)

    prompt = commands.add_parser("prompt", help="print a brief's prompt, to give to any agent by hand")
    prompt.add_argument("--brief", required=True)
    prompt.add_argument("--dir", required=True, help="folder the agent should write into")
    prompt.set_defaults(handler=command_prompt)

    check = commands.add_parser("check", help="check and render a folder an agent has already filled")
    check.add_argument("folder")
    check.add_argument("--brief", help="brief id; defaults to the folder's name")
    check.add_argument("--runner", default="manual", help="who made it, for the sheet's title and result.json")
    check.set_defaults(handler=command_check)

    compare = commands.add_parser("compare", help="put several runs' directions on one sheet")
    compare.add_argument("runs", nargs="+", help="run folders, each evals/out/<run>/<brief>")
    compare.add_argument("--blind", action="store_true", help="shuffle, label A, B, C and seal the mapping")
    compare.add_argument("--out", default=str(EVALS / "out"))
    compare.set_defaults(handler=command_compare)

    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())

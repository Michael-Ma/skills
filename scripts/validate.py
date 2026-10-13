"""Check distributable skill metadata, local file references and the direction deal, not design quality."""
import importlib.util
import itertools
from pathlib import Path
import random
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKDOWN_LINK = re.compile(r"\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Carried by more than one skill so that each installs on its own; the copies must not drift.
SHARED = ("references/divergence.md", "scripts/draw_axes.py")
TABLE_ROW = re.compile(r"^\| ([^|]+?) \| ([^|]+?) \|$", re.MULTILINE)


def check_shared(root: Path) -> list[str]:
    errors = []
    for name in SHARED:
        copies = sorted((root / "skills").glob(f"*/{name}"))
        if len({copy.read_bytes() for copy in copies}) > 1:
            listed = ", ".join(str(copy.relative_to(root)) for copy in copies)
            errors.append(f"{name}: copies differ: {listed}")
    return errors


def check_deal(root: Path, seeds: int = 200) -> list[str]:
    """The deal keeps the promises divergence.md makes about it, and the two list the same values."""
    errors = []
    for script in sorted((root / "skills").glob("*/scripts/draw_axes.py")):
        relative = script.relative_to(root)
        spec = importlib.util.spec_from_file_location("draw_axes", script)
        module = importlib.util.module_from_spec(spec)
        sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            errors.append(f"{relative}: does not load: {exc}")
            continue
        for seed in range(seeds):
            rng = random.Random(seed)
            sets = module.deal(rng)
            marked = module.mark_open(sets, rng)
            again = random.Random(seed)
            if module.mark_open(module.deal(again), again) != marked:
                errors.append(f"{relative}: seed {seed} does not repeat its deal")
                break
            if any(module.shared(a, b) > module.MAX_SHARED for a, b in itertools.combinations(sets, 2)):
                errors.append(f"{relative}: seed {seed} deals sets sharing more than {module.MAX_SHARED} values")
                break
            cells = [(i, axis) for i, values in enumerate(marked) for axis, value in values.items() if value == module.OPEN]
            spread = len({i for i, _ in cells}) == len({axis for _, axis in cells}) == module.OPEN_COUNT
            if len(cells) != module.OPEN_COUNT or not spread or any(axis not in module.OPEN_AXES for _, axis in cells):
                errors.append(f"{relative}: seed {seed} places its open positions wrongly")
                break
        guide = script.parent.parent / "references" / "divergence.md"
        if not guide.exists():
            errors.append(f"{relative}: no references/divergence.md beside it")
            continue
        rows = dict(TABLE_ROW.findall(guide.read_text(encoding="utf-8")))
        for axis, values in module.AXES.items():
            if [value.strip() for value in rows.get(axis, "").split(" · ")] != values:
                errors.append(f"{guide.relative_to(root)}: table row \"{axis}\" differs from {relative.name}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found under skills/<name>/SKILL.md")
    for entry in skills:
        relative = entry.relative_to(root)
        text = entry.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
        if not frontmatter:
            errors.append(f"{relative}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(frontmatter.group(1))
        except yaml.YAMLError as exc:
            errors.append(f"{relative}: invalid YAML: {exc}")
            continue
        if not isinstance(meta, dict):
            errors.append(f"{relative}: frontmatter must be a mapping")
            continue
        name, description = meta.get("name"), meta.get("description")
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{relative}: invalid skill name")
        elif name != entry.parent.name:
            errors.append(f"{relative}: name does not match folder")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{relative}: description must contain 1–1024 characters")
        if not text[frontmatter.end():].strip():
            errors.append(f"{relative}: empty skill instructions")

        ui_path = entry.parent / "agents" / "openai.yaml"
        if ui_path.exists():
            try:
                ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
                interface = ui.get("interface") if isinstance(ui, dict) else None
                if not isinstance(interface, dict):
                    errors.append(f"{ui_path.relative_to(root)}: missing interface mapping")
                else:
                    for key in ("display_name", "short_description", "default_prompt"):
                        if not isinstance(interface.get(key), str) or not interface[key].strip():
                            errors.append(f"{ui_path.relative_to(root)}: missing {key}")
            except yaml.YAMLError as exc:
                errors.append(f"{ui_path.relative_to(root)}: invalid YAML: {exc}")

    docs = [root / "README.md", *(root / "docs").rglob("*.md"), *(root / "skills").rglob("*.md")]
    for doc in docs:
        if not doc.exists():
            errors.append(f"Missing document: {doc.relative_to(root)}")
            continue
        text = doc.read_text(encoding="utf-8")
        # Examples may include placeholder paths; check authored Markdown links only.
        text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text)
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            destination = (doc.parent / path).resolve()
            if Path(path).is_absolute() or not destination.is_relative_to(root):
                errors.append(f"{doc.relative_to(root)}: non-portable local link {target}")
            elif not destination.exists():
                errors.append(f"{doc.relative_to(root)}: missing local link {target}")
    return errors + check_shared(root) + check_deal(root)


if __name__ == "__main__":
    failures = validate(ROOT)
    if failures:
        print("\n".join(f"ERROR: {message}" for message in failures), file=sys.stderr)
        raise SystemExit(1)
    count = len(list((ROOT / "skills").glob("*/SKILL.md")))
    print(f"Validated {count} skills: metadata, local file references and the direction deal pass.")

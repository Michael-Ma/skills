"""Check distributable skill metadata, local file references and the direction deal, not design quality."""
import importlib.util
import itertools
from pathlib import Path
import random
import re
import struct
import sys
import tempfile
import zlib
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKDOWN_LINK = re.compile(r"\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Carried by more than one skill so that each installs on its own; the copies must not drift.
SHARED = ("references/divergence.md", "scripts/draw_axes.py", "scripts/likeness.py")
TABLE_ROW = re.compile(r"^\| ([^|]+?) \| ([^|]+?) \|$", re.MULTILINE)


def check_shared(root: Path) -> list[str]:
    errors = []
    for name in SHARED:
        copies = sorted((root / "skills").glob(f"*/{name}"))
        if len({copy.read_bytes() for copy in copies}) > 1:
            listed = ", ".join(str(copy.relative_to(root)) for copy in copies)
            errors.append(f"{name}: copies differ: {listed}")
    return errors


def deck_table(text: str, deck: str) -> dict[str, list[str]]:
    """The rows of divergence.md's table for one deck: axis -> listed values."""
    match = re.search(rf"^\| Axis \| {deck.capitalize()} deck \|\n\|[-|]+\|\n((?:\|.*\|\n?)+)", text, re.MULTILINE)
    rows = TABLE_ROW.findall(match.group(1)) if match else []
    return {axis: [value.strip() for value in column.split(" · ")] for axis, column in rows}


def check_deal(root: Path, seeds: int = 200) -> list[str]:
    """The deal keeps the promises divergence.md makes about it, in every deck, and the two list the same values."""
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
        for deck, axes in module.DECKS.items():
            grounded = deck in module.GROUNDED_DECKS

            def allowed(axis: str, value: str) -> bool:
                return value in axes[axis] or (grounded and axis == module.STRUCTURE and value == module.USUAL)

            for seed in range(seeds):
                usual = module.STRUCTURES[seed % len(module.STRUCTURES)] if grounded else None
                rng = random.Random(seed)
                sets = module.deal(rng, deck, usual)
                cards = [(axis, f"sample {n}") for n, axis in enumerate(module.card_axes(deck)[: seed % 6])]
                marked = module.place_subject(sets, cards, rng, deck)
                again = random.Random(seed)
                if module.place_subject(module.deal(again, deck, usual), cards, again, deck) != marked:
                    errors.append(f"{relative}: {deck} seed {seed} does not repeat its deal")
                    break
                if any(module.shared(a, b) > module.MAX_SHARED for a, b in itertools.combinations(sets, 2)):
                    errors.append(f"{relative}: {deck} seed {seed} deals sets sharing more than {module.MAX_SHARED} values")
                    break
                if any(len({values[axis] for values in sets}) < len(sets) for axis in module.DISTINCT_AXES[deck]):
                    errors.append(f"{relative}: {deck} seed {seed} repeats a value on an axis that must differ")
                    break
                if any(list(values) != list(axes) or not all(allowed(axis, values[axis]) for axis in values) for values in sets):
                    errors.append(f"{relative}: {deck} seed {seed} deals a value from outside its deck")
                    break
                if grounded:
                    stretches = [values[module.STRUCTURE] for values in sets if values[module.STRUCTURE] != module.USUAL]
                    printed = module.describe(seed, cards, deck, usual)
                    alike = [values for values in sets if values[module.STRUCTURE] == module.USUAL]
                    if (len(stretches) != 1 or stretches[0] == usual or printed.count("(stretch)") != 1
                            or module.shared(*alike) != 1):
                        errors.append(f"{relative}: {deck} seed {seed} does not keep the usual layout, and nothing else in common, in two sets "
                                      "and deal one stretch a different structure")
                        break
                changed = [[axis for axis in values if values[axis] != before[axis]] for before, values in zip(sets, marked)]
                placed = [(axis, values[axis]) for values, axes_changed in zip(marked, changed) for axis in axes_changed]
                dealt_cards = [(axis, value[len(module.CARD):]) for axis, value in placed if value.startswith(module.CARD)]
                opens = [axis for axis, value in placed if value == module.OPEN]
                one_each = all(len(axes_changed) == 1 for axes_changed in changed)
                cards_first = len(dealt_cards) == min(len(cards), len(sets)) and len(set(dealt_cards)) == len(dealt_cards)
                valid = all(card in cards for card in dealt_cards) and all(axis in module.OPEN_AXES[deck] for axis in opens)
                if not (one_each and cards_first and valid and len(dealt_cards) + len(opens) == len(sets)):
                    errors.append(f"{relative}: {deck} seed {seed} does not give each set one card or open position")
                    break
            if grounded:
                try:
                    module.parse_card(f"{module.STRUCTURE}=sample", deck)
                    errors.append(f"{relative}: the {deck} deck accepts a card on structure")
                except ValueError:
                    pass
        guide = script.parent.parent / "references" / "divergence.md"
        if not guide.exists():
            errors.append(f"{relative}: no references/divergence.md beside it")
            continue
        text = guide.read_text(encoding="utf-8")
        for deck, axes in module.DECKS.items():
            listed = deck_table(text, deck)
            if not listed:
                errors.append(f"{guide.relative_to(root)}: no table for the {deck} deck")
                continue
            for axis in sorted(set(axes) | set(listed)):
                if listed.get(axis) != axes.get(axis):
                    errors.append(f"{guide.relative_to(root)}: {deck} deck row \"{axis}\" differs from {relative.name}")
    return errors


def png(rows: list[list[int]]) -> bytes:
    """A greyscale picture as an 8-bit RGB PNG, unfiltered."""
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    raw = b"".join(b"\0" + bytes(v for value in row for v in (value, value, value)) for row in rows)
    header = struct.pack(">IIBBBBB", len(rows[0]), len(rows), 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def check_likeness(root: Path) -> list[str]:
    """likeness.py reads a PNG, scores a page against itself as one layout and a different arrangement below ALIKE."""
    errors = []
    size = 192

    def page(text_at) -> list[list[int]]:
        # white ground with striped "text" where text_at(x, y) is true
        return [[0 if text_at(x, y) and y % 6 < 3 else 255 for x in range(size)] for y in range(size * 2)]

    sidebar = page(lambda x, y: x < size // 3 or (x > size // 2 and y < size // 2))
    banner = page(lambda x, y: y < size // 3 or (x > size // 4 and x < size * 3 // 4 and y > size))
    for script in sorted((root / "skills").glob("*/scripts/likeness.py")):
        relative = script.relative_to(root)
        spec = importlib.util.spec_from_file_location("likeness", script)
        module = importlib.util.module_from_spec(spec)
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
            with tempfile.TemporaryDirectory() as folder:
                first, second = Path(folder) / "a.png", Path(folder) / "b.png"
                first.write_bytes(png(sidebar))
                second.write_bytes(png(banner))
                a, b = module.content_grid(first), module.content_grid(second)
                same, different = module.likeness(a, a), module.likeness(a, b)
        except Exception as exc:
            errors.append(f"{relative}: does not run: {exc}")
            continue
        if same < 0.999 or different >= module.ALIKE:
            errors.append(f"{relative}: scores a page against itself {same:.2f} and a different layout {different:.2f}")
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

    # evals/out holds agents' own files and is not part of the collection
    docs = [root / "README.md", *(root / "docs").rglob("*.md"), *(root / "skills").rglob("*.md"),
            *(root / "evals").glob("*.md"), *(root / "evals" / "briefs").glob("*.md")]
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
    return errors + check_shared(root) + check_deal(root) + check_likeness(root)


if __name__ == "__main__":
    failures = validate(ROOT)
    if failures:
        print("\n".join(f"ERROR: {message}" for message in failures), file=sys.stderr)
        raise SystemExit(1)
    count = len(list((ROOT / "skills").glob("*/SKILL.md")))
    print(f"Validated {count} skills: metadata, local file references and the direction deal pass.")

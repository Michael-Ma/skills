#!/usr/bin/env python3
"""Deal axis values for three divergent visual directions.

Usage:
  python3 draw_axes.py                                   deal three sets and print the seed
  python3 draw_axes.py --seed 205960                     repeat a recorded deal
  python3 draw_axes.py --axis "Canvas" --exclude "dark"  redraw one value
"""
from __future__ import annotations

import argparse
import itertools
import random
import time

AXES = {
    "Structure of the primary object": [
        "list or table",
        "grid of tiles",
        "a continuous timeline or chart that is the interface",
        "one focal item with the rest subordinate",
        "map or diagram",
    ],
    "Canvas": ["light neutral", "dark", "a saturated color field", "white with one vivid hue"],
    "Type": [
        "condensed or signage sans",
        "geometric or humanist sans",
        "serif-led",
        "monospace or tabular-led",
    ],
    "Scale and density": ["compact reference", "comfortable", "poster-scale with few elements"],
    "Shape language": [
        "ruled and square",
        "soft and rounded",
        "heavy blocks and fills",
        "fine line and diagram",
    ],
    "Color": [
        "status only",
        "one brand color carrying identity",
        "several hues carrying categories",
    ],
    "Source world": [
        "the subject's own print tradition",
        "an instrument or control surface",
        "signage and wayfinding",
        "editorial or magazine",
        "a consumer product from an unrelated category",
    ],
}
# Axes where a value from the subject's own world can replace a listed one.
OPEN_AXES = ("Structure of the primary object", "Canvas", "Type", "Shape language", "Source world")
OPEN = "open"
MAX_SHARED = 2
OPEN_COUNT = 2


def shared(a: dict[str, str], b: dict[str, str]) -> int:
    """Number of axes on which two sets carry the same value."""
    return sum(a[axis] == b[axis] for axis in AXES)


def deal(rng: random.Random) -> list[dict[str, str]]:
    """Three sets of values; no two sets share more than MAX_SHARED values."""
    while True:
        sets = [{axis: rng.choice(values) for axis, values in AXES.items()} for _ in range(3)]
        if all(shared(a, b) <= MAX_SHARED for a, b in itertools.combinations(sets, 2)):
            return sets


def mark_open(sets: list[dict[str, str]], rng: random.Random) -> list[dict[str, str]]:
    """Blank OPEN_COUNT positions, on different directions and different axes."""
    directions = rng.sample(range(len(sets)), OPEN_COUNT)
    axes = rng.sample(OPEN_AXES, OPEN_COUNT)
    marked = [dict(values) for values in sets]
    for direction, axis in zip(directions, axes):
        marked[direction][axis] = OPEN
    return marked


def redraw(axis: str, exclude: str | None, rng: random.Random) -> str:
    """One new value for an axis, different from the excluded one."""
    return rng.choice([value for value in AXES[axis] if value != exclude])


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--seed", type=int, help="repeat a recorded deal")
    parser.add_argument("--axis", help="redraw a single axis")
    parser.add_argument("--exclude", help="value the redraw must avoid")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time() * 1000) % 1_000_000
    rng = random.Random(seed)
    print(f"seed {seed}")

    if args.axis:
        if args.axis not in AXES:
            raise SystemExit("unknown axis; choose one of: " + "; ".join(AXES))
        print(f"{args.axis}: {redraw(args.axis, args.exclude, rng)}")
        return

    for number, values in enumerate(mark_open(deal(rng), rng), 1):
        print(f"\nDirection {number}")
        for axis, value in values.items():
            if value == OPEN:
                value = "open (supply a value from the subject's own world that is not in the table)"
            print(f"  {axis}: {value}")


if __name__ == "__main__":
    main()

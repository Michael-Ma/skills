#!/usr/bin/env python3
"""Deal axis values for three divergent visual directions.

Usage:
  python3 draw_axes.py --card "Canvas=kraft board" --card "Type=stencil lettering" ...
                                                         deal three sets; each carries one card
  python3 draw_axes.py --seed 205960 --card ...          repeat a recorded deal (same cards, same order)
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
# Axes where a set without a card may ask for one to be written on the spot.
OPEN_AXES = ("Structure of the primary object", "Canvas", "Type", "Shape language", "Source world")
OPEN = "open"
CARD = "card: "
MAX_SHARED = 2


def shared(a: dict[str, str], b: dict[str, str]) -> int:
    """Number of axes on which two sets carry the same value."""
    return sum(a[axis] == b[axis] for axis in AXES)


def deal(rng: random.Random) -> list[dict[str, str]]:
    """Three sets of values; no two sets share more than MAX_SHARED values."""
    while True:
        sets = [{axis: rng.choice(values) for axis, values in AXES.items()} for _ in range(3)]
        if all(shared(a, b) <= MAX_SHARED for a, b in itertools.combinations(sets, 2)):
            return sets


def parse_card(text: str) -> tuple[str, str]:
    """Split 'Axis=value', matching the axis name without regard to case."""
    axis, separator, value = text.partition("=")
    names = {name.casefold(): name for name in AXES}
    key = axis.strip().casefold()
    if not separator or not value.strip() or key not in names:
        raise ValueError(f'"{text}" is not "<axis>=<value>"; axes are: ' + "; ".join(AXES))
    return names[key], value.strip()


def place_subject(
    sets: list[dict[str, str]], cards: list[tuple[str, str]], rng: random.Random
) -> list[dict[str, str]]:
    """Give every set one position from the subject: a card while they last, otherwise open."""
    chosen = rng.sample(cards, min(len(cards), len(sets)))
    order = rng.sample(range(len(sets)), len(sets))
    placed = [dict(values) for values in sets]
    for position, direction in enumerate(order):
        if position < len(chosen):
            axis, value = chosen[position]
            placed[direction][axis] = CARD + value
        else:
            placed[direction][rng.choice(OPEN_AXES)] = OPEN
    return placed


def redraw(axis: str, exclude: str | None, rng: random.Random) -> str:
    """One new value for an axis, different from the excluded one."""
    return rng.choice([value for value in AXES[axis] if value != exclude])


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--card", action="append", default=[], metavar="AXIS=VALUE",
                        help="a subject card written before the deal; repeat for each card")
    parser.add_argument("--seed", type=int, help="repeat a recorded deal")
    parser.add_argument("--axis", help="redraw a single axis")
    parser.add_argument("--exclude", help="value the redraw must avoid")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time() * 1000) % 1_000_000
    rng = random.Random(seed)

    if args.axis:
        if args.axis not in AXES:
            raise SystemExit("unknown axis; choose one of: " + "; ".join(AXES))
        print(f"seed {seed}")
        print(f"{args.axis}: {redraw(args.axis, args.exclude, rng)}")
        return

    try:
        cards = [parse_card(text) for text in args.card]
    except ValueError as error:
        raise SystemExit(str(error))

    print(f"seed {seed}")
    for number, values in enumerate(place_subject(deal(rng), cards, rng), 1):
        print(f"\nDirection {number}")
        for axis, value in values.items():
            if value == OPEN:
                value = "open (write a card for this axis now, from the subject's own world)"
            elif value.startswith(CARD):
                value = "[card] " + value[len(CARD):]
            print(f"  {axis}: {value}")


if __name__ == "__main__":
    main()

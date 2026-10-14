#!/usr/bin/env python3
"""Deal axis values for three divergent visual directions.

Usage:
  python3 draw_axes.py --usual "list or table" --card "Lead=the cut-off countdown" ...
                                                deal three sets from the product deck; each carries one card
  python3 draw_axes.py --deck expressive --card ...   deal from the expressive deck
  python3 draw_axes.py --seed 205960 --usual ... --card ...   repeat a recorded deal (same deck, usual, cards and order)
  python3 draw_axes.py --axis "Lead" --exclude "the content itself"   redraw one value from the product deck
"""
from __future__ import annotations

import argparse
import itertools
import random
import time

STRUCTURE = "Structure of the primary object"
STRUCTURES = [
    "list or table",
    "grid of tiles",
    "a continuous timeline or chart that is the interface",
    "one focal item with the rest subordinate",
    "map or diagram",
]
SOURCES = [
    "the subject's own print tradition",
    "an instrument or control surface",
    "signage and wayfinding",
    "editorial or magazine",
    "a consumer product from an unrelated category",
]
# Products in one category share a layout and differ inside it, so the product deck keeps the
# category's usual layout in two directions and deals the rest; one stretch direction is dealt a
# different structure. Canvas and type follow the category and are not dealt.
# The expressive deck is for brand-led pages, or when the person asks for something bold.
DECKS = {
    "product": {
        STRUCTURE: STRUCTURES,  # dealt to the stretch only, never the category's usual one
        "Lead": [
            "the recommended choice",
            "what needs an answer",
            "the limit being worked to",
            "the running total or progress",
            "the content itself",
        ],
        "Item anatomy": [
            "one line with a trailing value",
            "two lines with labels or badges",
            "an inline bar or timeline in each item",
            "choices inline in each item",
            "collapsed items that expand in place",
        ],
        "Scale and density": ["compact", "comfortable", "spacious with one prominent element"],
        "Shape language": [
            "platform-native controls",
            "cards with clear hierarchy",
            "ruled lists and tables",
            "soft and rounded",
        ],
        "Color": [
            "neutral with one accent",
            "status colors only",
            "one brand color carrying identity",
            "several hues carrying categories",
        ],
        "Borrowed from another category": [
            "a banking or payments app",
            "a grocery or food delivery app",
            "a messaging app",
            "a maps or navigation app",
            "a calendar or booking app",
            "a review and approval tool",
            "a fitness or health tracker",
        ],
    },
    "expressive": {
        STRUCTURE: STRUCTURES,
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
        "Source world": SOURCES,
    },
}
DEFAULT_DECK = "product"
# Decks where two directions keep the category's usual layout and one stretch is dealt another.
GROUNDED_DECKS = ("product",)
USUAL = "the category's usual layout"
# Axes on which no value repeats within a deal.
DISTINCT_AXES = {
    "product": ("Lead", "Item anatomy"),
    "expressive": (STRUCTURE, "Canvas"),
}
# Axes where a set without a card may ask for one to be written on the spot.
OPEN_AXES = {
    "product": ("Lead", "Item anatomy", "Shape language", "Borrowed from another category"),
    "expressive": (STRUCTURE, "Canvas", "Type", "Shape language", "Source world"),
}
OPEN = "open"
CARD = "card: "
MAX_SHARED = 2


def shared(a: dict[str, str], b: dict[str, str]) -> int:
    """Number of axes on which two sets carry the same value."""
    return sum(a[axis] == b[axis] for axis in a)


def deal(rng: random.Random, deck: str = DEFAULT_DECK, usual: str | None = None) -> list[dict[str, str]]:
    """Three sets of values. No two share more than MAX_SHARED, and none repeats on the deck's distinct axes.

    In a grounded deck two sets keep USUAL as their structure and share no other value, and one,
    the stretch, is dealt a structure other than `usual`.
    """
    axes = DECKS[deck]
    while True:
        sets = [{axis: rng.choice(values) for axis, values in axes.items()} for _ in range(3)]
        if deck in GROUNDED_DECKS:
            stretch = rng.randrange(len(sets))
            for number, values in enumerate(sets):
                values[STRUCTURE] = rng.choice([s for s in STRUCTURES if s != usual]) if number == stretch else USUAL
        apart = all(shared(a, b) <= MAX_SHARED for a, b in itertools.combinations(sets, 2))
        if deck in GROUNDED_DECKS:
            # the two that share a layout have to differ everywhere else
            apart = apart and shared(*[values for values in sets if values[STRUCTURE] == USUAL]) == 1
        if apart and all(len({values[axis] for values in sets}) == len(sets) for axis in DISTINCT_AXES[deck]):
            return sets


def card_axes(deck: str) -> list[str]:
    """Axes a card may sit on. In a grounded deck structure is the category's or the stretch's, never a card's."""
    return [axis for axis in DECKS[deck] if not (deck in GROUNDED_DECKS and axis == STRUCTURE)]


def parse_card(text: str, deck: str = DEFAULT_DECK) -> tuple[str, str]:
    """Split 'Axis=value', matching the axis name without regard to case."""
    axis, separator, value = text.partition("=")
    names = {name.casefold(): name for name in card_axes(deck)}
    key = axis.strip().casefold()
    if not separator or not value.strip() or key not in names:
        hint = ""
        if deck in GROUNDED_DECKS and key in ("canvas", "type", STRUCTURE.casefold()):
            hint = (" In the product deck canvas and type follow the category and structure is the category's"
                    " or the stretch's; put the idea on another axis, or use the expressive deck.")
        raise ValueError(f'"{text}" is not "<axis>=<value>" for the {deck} deck; its card axes are: '
                         + "; ".join(card_axes(deck)) + "." + hint)
    return names[key], value.strip()


def place_subject(
    sets: list[dict[str, str]], cards: list[tuple[str, str]], rng: random.Random, deck: str = DEFAULT_DECK
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
            placed[direction][rng.choice(OPEN_AXES[deck])] = OPEN
    return placed


def redraw(axis: str, exclude: str | None, rng: random.Random, deck: str = DEFAULT_DECK,
           usual: str | None = None) -> str:
    """One new value for an axis, different from the excluded one and, for structure, from the usual one."""
    return rng.choice([value for value in DECKS[deck][axis] if value not in (exclude, usual)])


def describe(seed: int, cards: list[tuple[str, str]], deck: str = DEFAULT_DECK, usual: str | None = None) -> str:
    """The printed form of a deal. The same seed, deck, usual layout and cards, in the same order, give the same text."""
    rng = random.Random(seed)
    lines = [f"seed {seed}", f"deck: {deck}"]
    if deck in GROUNDED_DECKS:
        lines.append(f"usual: {usual}")
    lines += [f"card: {axis}={value}" for axis, value in cards]
    for number, values in enumerate(place_subject(deal(rng, deck, usual), cards, rng, deck), 1):
        stretch = deck in GROUNDED_DECKS and values[STRUCTURE] != USUAL
        lines += ["", f"Direction {number}" + (" (stretch)" if stretch else "")]
        for axis, value in values.items():
            if value == OPEN:
                value = "open (write a card for this axis now, from this brief)"
            elif value.startswith(CARD):
                value = "[card] " + value[len(CARD):]
            elif value == USUAL:
                value = f"{USUAL} ({usual})"
            lines.append(f"  {axis}: {value}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--deck", choices=sorted(DECKS), default=DEFAULT_DECK,
                        help="product (default) for app and tool screens; expressive for brand-led pages")
    parser.add_argument("--usual", choices=STRUCTURES, metavar="STRUCTURE",
                        help="product deck: the listed structure closest to how this category's products lay out "
                             "the screen; the stretch is dealt a different one. One of: " + "; ".join(STRUCTURES))
    parser.add_argument("--card", action="append", default=[], metavar="AXIS=VALUE",
                        help="a subject card written before the deal; repeat for each card")
    parser.add_argument("--seed", type=int, help="repeat a recorded deal")
    parser.add_argument("--axis", help="redraw a single axis")
    parser.add_argument("--exclude", help="value the redraw must avoid")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time() * 1000) % 1_000_000
    rng = random.Random(seed)

    if args.axis:
        if args.axis not in DECKS[args.deck]:
            raise SystemExit(f"unknown axis for the {args.deck} deck; choose one of: " + "; ".join(DECKS[args.deck]))
        print(f"seed {seed}")
        print(f"{args.axis}: {redraw(args.axis, args.exclude, rng, args.deck, args.usual)}")
        return

    if args.deck in GROUNDED_DECKS and not args.usual:
        raise SystemExit("the product deck needs --usual: the listed structure closest to how products in this "
                         "category lay out this screen. One of: " + "; ".join(STRUCTURES))
    try:
        cards = [parse_card(text, args.deck) for text in args.card]
    except ValueError as error:
        raise SystemExit(str(error))
    print(describe(seed, cards, args.deck, args.usual))


if __name__ == "__main__":
    main()

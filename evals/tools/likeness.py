"""How alike two rendered studies are in layout, with color, tone and spacing set aside.

Each render becomes a grid of where its content sits: the page is cut into small square cells and
each cell gets the spread of its grey values, high where there is text, an edge or a control, low
on plain ground, so a light and a dark version of one layout give nearly the same grid. Each row
of cells, a band, is compared by the shape of its profile across the page. The two pages' bands
are then aligned top to bottom, letting one stretch against the other, so a list with roomier rows
still matches the same list set tighter. The likeness is one minus the average cost of that
alignment: near 1 when the two read as one layout, lower as the arrangement differs.

ALIKE was set on the author's eval runs: at 0.86 it flagged five of eight pairs judged to be
one layout and one of 45 judged distinct. It is an aid to a person's judgment, not a measure
of taste.

Standard library only, so the eval runs without installing anything.
"""
from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

FINE_ACROSS = 48  # cells across the page when measuring
POOL = 3  # cells merged each way when comparing, so 16 across
BLANK = 4.0  # a band with less content than this is plain ground
ALIKE = 0.86


def read_png_grey(path: Path, width: int | None = None) -> tuple[int, int, list[bytearray]]:
    """Rows of 0-255 grey values from an 8-bit, non-interlaced RGB or RGBA PNG, cropped to `width`."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.name}: not a PNG")
    position, chunks, header = 8, [], None
    while position < len(data):
        length, kind = struct.unpack(">I4s", data[position:position + 8])
        body = data[position + 8:position + 8 + length]
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            chunks.append(body)
        position += 12 + length
    full_width, height, depth, color, _, _, interlace = header
    channels = {2: 3, 6: 4}.get(color)
    if depth != 8 or channels is None or interlace:
        raise ValueError(f"{path.name}: only 8-bit non-interlaced RGB or RGBA PNGs are read")
    raw = zlib.decompress(b"".join(chunks))
    stride = full_width * channels
    keep = min(width or full_width, full_width)
    previous = bytearray(stride)
    rows = []
    for y in range(height):
        start = y * (stride + 1)
        kind, line = raw[start], bytearray(raw[start + 1:start + 1 + stride])
        if kind == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 255
        elif kind == 2:
            line = bytearray((a + b) & 255 for a, b in zip(line, previous))
        elif kind == 3:
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + previous[i]) >> 1)) & 255
        elif kind == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b, c = previous[i], previous[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        previous = line
        rows.append(bytearray((299 * line[x] + 587 * line[x + 1] + 114 * line[x + 2]) // 1000
                              for x in range(0, keep * channels, channels)))
    return keep, height, rows


def content_grid(path: Path, width: int | None = None) -> list[list[float]]:
    """Spread of grey values per cell, FINE_ACROSS cells across, merged POOL by POOL."""
    page_width, height, rows = read_png_grey(path, width)
    cell = page_width / FINE_ACROSS
    fine = []
    top = 0.0
    while top + cell <= height:
        band = []
        for column in range(FINE_ACROSS):
            x0, x1, y0, y1 = int(column * cell), int((column + 1) * cell), int(top), int(top + cell)
            # every second pixel each way is plenty for a spread, and four times quicker
            sample = [rows[y][x] for y in range(y0, y1, 2) for x in range(x0, x1, 2)]
            mean = sum(sample) / len(sample)
            band.append(math.sqrt(sum((v - mean) ** 2 for v in sample) / len(sample)))
        fine.append(band)
        top += cell
    return [[sum(fine[r + i][c + j] for i in range(POOL) for j in range(POOL)) / POOL ** 2
             for c in range(0, FINE_ACROSS - POOL + 1, POOL)]
            for r in range(0, len(fine) - POOL + 1, POOL)]


def bands(grid: list[list[float]]) -> list[list[float] | None]:
    """Each band's profile scaled to unit length, or None for plain ground."""
    shaped = []
    for band in grid:
        size = math.sqrt(sum(v * v for v in band))
        shaped.append([v / size for v in band] if size > BLANK else None)
    return shaped


def _cost(a: list[float] | None, b: list[float] | None) -> float:
    if a is None or b is None:
        return 0.0 if a is b else 1.0
    return 1.0 - sum(x * y for x, y in zip(a, b))


def likeness(a: list[list[float]], b: list[list[float]]) -> float:
    """1 minus the mean cost of the best top-to-bottom alignment of two pages' bands."""
    first, second = bands(a), bands(b)
    n, m = len(first), len(second)
    if not n or not m:
        return 0.0
    total = [[math.inf] * (m + 1) for _ in range(n + 1)]
    steps = [[0] * (m + 1) for _ in range(n + 1)]
    total[0][0] = 0.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost, length = min((total[i - 1][j - 1], steps[i - 1][j - 1]),
                               (total[i - 1][j], steps[i - 1][j]),
                               (total[i][j - 1], steps[i][j - 1]))
            total[i][j] = cost + _cost(first[i - 1], second[j - 1])
            steps[i][j] = length + 1
    return 1.0 - total[n][m] / steps[n][m]

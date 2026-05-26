#!/usr/bin/env python3
"""Decode a published Google Doc containing (char, x, y) rows into a text grid."""

from __future__ import annotations

import re
import sys
from html import unescape
from typing import Iterable
from urllib.request import urlopen


TD_PATTERN = re.compile(r"<td[^>]*>(.*?)</td>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


def _extract_cells(html: str) -> list[str]:
    """Return all table-cell text values from the published Google Doc HTML."""
    cells: list[str] = []
    for match in TD_PATTERN.finditer(html):
        raw = match.group(1)
        text = unescape(TAG_PATTERN.sub("", raw)).strip()
        cells.append(text)
    return cells


def _parse_rows(cells: Iterable[str]) -> list[tuple[str, int, int]]:
    """Parse flattened cell values into (char, x, y) triples."""
    values = list(cells)
    if len(values) < 3:
        raise ValueError("No table data found in the document.")

    triples: list[tuple[str, int, int]] = []

    # Data appears as repeating 3-cell rows, often with a header row.
    for i in range(0, len(values) - 2, 3):
        a, b, c = values[i], values[i + 1], values[i + 2]
        try:
            x = int(b)
            y = int(c)
        except ValueError:
            # Skip header or non-data rows.
            continue

        if not a:
            # Empty character entries are not useful for drawing.
            continue

        triples.append((a[0], x, y))

    if not triples:
        raise ValueError("No valid (character, x, y) rows were parsed.")

    return triples


def render_doc_grid(url: str) -> str:
    """Fetch, parse, and render the character grid from a published Google Doc URL."""
    with urlopen(url) as response:
        html = response.read().decode("utf-8", errors="replace")

    cells = _extract_cells(html)
    points = _parse_rows(cells)

    max_x = max(x for _, x, _ in points)
    max_y = max(y for _, _, y in points)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for char, x, y in points:
        grid[y][x] = char

    return "\n".join("".join(row) for row in grid)


def print_doc_grid(url: str) -> None:
    """Convenience wrapper that prints the decoded grid."""
    print(render_doc_grid(url))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <published-google-doc-url>", file=sys.stderr)
        raise SystemExit(2)
    print_doc_grid(sys.argv[1])

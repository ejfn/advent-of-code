#!/usr/bin/env python3
"""
Advent of Code 2023 Day 11: Cosmic Expansion
"""

from __future__ import annotations

import os
import sys
from itertools import combinations
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def galaxy_positions(lines: Iterable[str]) -> list[tuple[int, int]]:
    grid = list(lines)
    galaxies = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                galaxies.append((r, c))
    return galaxies


def expand_positions(galaxies: list[tuple[int, int]], lines: list[str], factor: int) -> list[tuple[int, int]]:
    height = len(lines)
    width = len(lines[0])

    empty_rows = [all(ch == "." for ch in lines[r]) for r in range(height)]
    empty_cols = [all(lines[r][c] == "." for r in range(height)) for c in range(width)]

    row_extra = [0] * height
    extra = 0
    for r in range(height):
        row_extra[r] = extra
        if empty_rows[r]:
            extra += factor - 1

    col_extra = [0] * width
    extra = 0
    for c in range(width):
        col_extra[c] = extra
        if empty_cols[c]:
            extra += factor - 1

    expanded = []
    for r, c in galaxies:
        expanded.append((r + row_extra[r], c + col_extra[c]))
    return expanded


def total_distance(points: list[tuple[int, int]]) -> int:
    total = 0
    for (r1, c1), (r2, c2) in combinations(points, 2):
        total += abs(r1 - r2) + abs(c1 - c2)
    return total


def solve(lines: Iterable[str], factor: int) -> int:
    grid = [line.rstrip("\n") for line in lines if line.strip()]
    galaxies = galaxy_positions(grid)
    expanded = expand_positions(galaxies, grid, factor)
    return total_distance(expanded)


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else list(lines)
    return solve(data, factor=2)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else list(lines)
    return solve(data, factor=1_000_000)


def run_example() -> None:
    example = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()
    assert solve(example, 2) == 374
    assert solve(example, 10) == 1030
    assert solve(example, 100) == 8410
    print("✓ Example checks passed")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

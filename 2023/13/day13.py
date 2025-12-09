#!/usr/bin/env python3
"""
Advent of Code 2023 Day 13: Point of Incidence
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List


def read_input() -> str:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_patterns(text: str) -> list[list[str]]:
    blocks = text.strip().split("\n\n")
    return [block.splitlines() for block in blocks]


def reflection_score(pattern: list[str], allowed_diff: int, horizontal: bool) -> int:
    rows = len(pattern)
    cols = len(pattern[0])

    if not horizontal:
        # transpose: treat columns as rows
        pattern = ["".join(pattern[r][c] for r in range(rows)) for c in range(cols)]
        rows, cols = cols, rows

    for split in range(1, rows):
        diff = 0
        for offset in range(min(split, rows - split)):
            upper = pattern[split - 1 - offset]
            lower = pattern[split + offset]
            diff += sum(1 for a, b in zip(upper, lower) if a != b)
            if diff > allowed_diff:
                break
        if diff == allowed_diff:
            return split
    return 0


def solve(patterns: list[list[str]], allowed_diff: int) -> int:
    total = 0
    for pattern in patterns:
        row = reflection_score(pattern, allowed_diff, horizontal=True)
        if row:
            total += 100 * row
            continue
        col = reflection_score(pattern, allowed_diff, horizontal=False)
        total += col
    return total


def part1(lines: Iterable[str] | None = None) -> int:
    text = read_input() if lines is None else "\n".join(lines)
    patterns = parse_patterns(text)
    return solve(patterns, allowed_diff=0)


def part2(lines: Iterable[str] | None = None) -> int:
    text = read_input() if lines is None else "\n".join(lines)
    patterns = parse_patterns(text)
    return solve(patterns, allowed_diff=1)


def run_example() -> None:
    example = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
    assert part1(example.strip().splitlines()) == 405
    assert part2(example.strip().splitlines()) == 400
    print("✓ Example checks passed (Part 1: 405, Part 2: 400)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

#!/usr/bin/env python3
"""
Advent of Code 2023 Day 3: Gear Ratios
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from typing import Iterable, Iterator, List, Tuple


Grid = List[str]


def read_input() -> Grid:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def iter_numbers(grid: Grid) -> Iterator[Tuple[int, int, int, int]]:
    """Yield (value, row, start_col, end_col)."""
    for y, line in enumerate(grid):
        x = 0
        while x < len(line):
            if line[x].isdigit():
                start = x
                while x < len(line) and line[x].isdigit():
                    x += 1
                value = int(line[start:x])
                yield value, y, start, x - 1
            else:
                x += 1


def in_bounds(grid: Grid, y: int, x: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def has_symbol_adjacent(grid: Grid, y: int, start: int, end: int) -> bool:
    for ny in range(y - 1, y + 2):
        for nx in range(start - 1, end + 2):
            if not in_bounds(grid, ny, nx):
                continue
            ch = grid[ny][nx]
            if ch != "." and not ch.isdigit():
                return True
    return False


def adjacent_gears(grid: Grid, y: int, start: int, end: int):
    gears = set()
    for ny in range(y - 1, y + 2):
        for nx in range(start - 1, end + 2):
            if not in_bounds(grid, ny, nx):
                continue
            if grid[ny][nx] == "*":
                gears.add((ny, nx))
    return gears


def part1(lines: Iterable[str] | None = None) -> int:
    grid = list(lines) if lines is not None else read_input()
    total = 0
    for value, y, start, end in iter_numbers(grid):
        if has_symbol_adjacent(grid, y, start, end):
            total += value
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    grid = list(lines) if lines is not None else read_input()
    gear_map: dict[tuple[int, int], list[int]] = defaultdict(list)
    for value, y, start, end in iter_numbers(grid):
        for gear in adjacent_gears(grid, y, start, end):
            gear_map[gear].append(value)
    total = 0
    for nums in gear_map.values():
        if len(nums) == 2:
            total += nums[0] * nums[1]
    return total


def run_example() -> None:
    example = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".splitlines()
    assert part1(example) == 4361
    assert part2(example) == 467835
    print("✓ Example checks passed (Part 1: 4361, Part 2: 467835)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

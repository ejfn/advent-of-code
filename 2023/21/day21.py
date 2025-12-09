#!/usr/bin/env python3
"""
Advent of Code 2023 Day 21: Step Counter
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Set, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def part1(lines: Iterable[str] | None = None, steps: int = 64) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    rows = len(grid)
    cols = len(grid[0])
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break
    assert start is not None

    current = {start}
    for _ in range(steps):
        nxt = set()
        for r, c in current:
            for nr, nc in neighbors(r, c):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                    nxt.add((nr, nc))
        current = nxt
    return len(current)


def infinite_reachable(grid: list[str], steps: int) -> int:
    size = len(grid)
    start = None
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break
    assert start is not None

    current = {start}
    for _ in range(steps):
        nxt = set()
        for x, y in current:
            for nx, ny in neighbors(x, y):
                rx = nx % size
                ry = ny % size
                if grid[rx][ry] != "#":
                    nxt.add((nx, ny))
        current = nxt
    return len(current)


def part2(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    size = len(grid)
    start = None
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "S":
                start = (r, c)
                break
        if start:
            break
    assert start is not None

    steps_target = 26501365
    base = size // 2
    assert (steps_target - base) % size == 0
    k_target = (steps_target - base) // size

    counts = []
    for i in range(3):
        steps = base + i * size
        counts.append(infinite_reachable(grid, steps))

    f0, f1, f2 = counts
    d1 = f1 - f0
    d2 = f2 - f1
    dd = d2 - d1

    def value_at(k: int) -> int:
        return f0 + k * d1 + (k * (k - 1) // 2) * dd

    return value_at(k_target)


def run_example() -> None:
    example = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""".splitlines()
    assert part1(example, steps=6) == 16
    print("✓ Example checks passed (Part 1 sample)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

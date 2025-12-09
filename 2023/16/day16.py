#!/usr/bin/env python3
"""
Advent of Code 2023 Day 16: The Floor Will Be Lava
"""

from __future__ import annotations

import os
import sys
from collections import deque
from typing import Iterable, List, Set, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


Grid = list[str]
State = tuple[int, int, int, int]


def traverse(grid: Grid, start: State) -> int:
    rows = len(grid)
    cols = len(grid[0])

    energized: Set[tuple[int, int]] = set()
    visited: Set[State] = set()
    queue = deque([start])

    while queue:
        r, c, dr, dc = queue.popleft()
        r += dr
        c += dc
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        state = (r, c, dr, dc)
        if state in visited:
            continue
        visited.add(state)
        energized.add((r, c))
        tile = grid[r][c]
        if tile == ".":
            queue.append((r, c, dr, dc))
        elif tile == "/":
            queue.append((r, c, -dc, -dr))
        elif tile == "\\":
            queue.append((r, c, dc, dr))
        elif tile == "|":
            if dc != 0:
                queue.append((r, c, -1, 0))
                queue.append((r, c, 1, 0))
            else:
                queue.append((r, c, dr, dc))
        elif tile == "-":
            if dr != 0:
                queue.append((r, c, 0, -1))
                queue.append((r, c, 0, 1))
            else:
                queue.append((r, c, dr, dc))
    return len(energized)


def part1(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    return traverse(grid, (0, -1, 0, 1))


def part2(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    rows = len(grid)
    cols = len(grid[0])
    best = 0
    for c in range(cols):
        best = max(best, traverse(grid, (-1, c, 1, 0)))
        best = max(best, traverse(grid, (rows, c, -1, 0)))
    for r in range(rows):
        best = max(best, traverse(grid, (r, -1, 0, 1)))
        best = max(best, traverse(grid, (r, cols, 0, -1)))
    return best


def run_example() -> None:
    example = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
""".splitlines()
    assert part1(example) == 46
    assert part2(example) == 51
    print("✓ Example checks passed (Part 1: 46, Part 2: 51)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

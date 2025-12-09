#!/usr/bin/env python3
"""
Advent of Code 2023 Day 14: Parabolic Reflector Dish
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def tilt(grid: list[list[str]], direction: str) -> None:
    rows = len(grid)
    cols = len(grid[0])

    if direction == "N":
        for c in range(cols):
            target = 0
            for r in range(rows):
                if grid[r][c] == "#":
                    target = r + 1
                elif grid[r][c] == "O":
                    if r != target:
                        grid[r][c] = "."
                        grid[target][c] = "O"
                    target += 1
    elif direction == "S":
        for c in range(cols):
            target = rows - 1
            for r in range(rows - 1, -1, -1):
                if grid[r][c] == "#":
                    target = r - 1
                elif grid[r][c] == "O":
                    if r != target:
                        grid[r][c] = "."
                        grid[target][c] = "O"
                    target -= 1
    elif direction == "W":
        for r in range(rows):
            target = 0
            for c in range(cols):
                if grid[r][c] == "#":
                    target = c + 1
                elif grid[r][c] == "O":
                    if c != target:
                        grid[r][c] = "."
                        grid[r][target] = "O"
                    target += 1
    elif direction == "E":
        for r in range(rows):
            target = cols - 1
            for c in range(cols - 1, -1, -1):
                if grid[r][c] == "#":
                    target = c - 1
                elif grid[r][c] == "O":
                    if c != target:
                        grid[r][c] = "."
                        grid[r][target] = "O"
                    target -= 1


def load(grid: list[list[str]]) -> int:
    rows = len(grid)
    total = 0
    for r in range(rows):
        weight = rows - r
        total += weight * sum(1 for ch in grid[r] if ch == "O")
    return total


def cycle(grid: list[list[str]]) -> None:
    for direction in ["N", "W", "S", "E"]:
        tilt(grid, direction)


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    grid = [list(row) for row in data]
    tilt(grid, "N")
    return load(grid)


def grid_state(grid: list[list[str]]) -> tuple[str, ...]:
    return tuple("".join(row) for row in grid)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    grid = [list(row) for row in data]

    seen: dict[tuple[str, ...], int] = {}
    states: list[tuple[str, ...]] = []
    total_cycles = 1_000_000_000
    cycle_idx = 0

    while cycle_idx < total_cycles:
        state = grid_state(grid)
        if state in seen:
            start = seen[state]
            loop_len = cycle_idx - start
            remaining = (total_cycles - start) % loop_len
            final_state = states[start + remaining]
            grid = [list(row) for row in final_state]
            return load(grid)
        seen[state] = cycle_idx
        states.append(state)
        cycle(grid)
        cycle_idx += 1

    return load(grid)


def run_example() -> None:
    example = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".splitlines()
    assert part1(example) == 136
    assert part2(example) == 64
    print("✓ Example checks passed (Part 1: 136, Part 2: 64)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

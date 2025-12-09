#!/usr/bin/env python3
"""
Advent of Code 2023 Day 10: Pipe Maze
"""

from __future__ import annotations

import os
import sys
from collections import deque
from typing import Dict, Iterable, List, Set, Tuple


DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}

OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

CONNECTIONS = {
    "|": {"N", "S"},
    "-": {"E", "W"},
    "L": {"N", "E"},
    "J": {"N", "W"},
    "7": {"S", "W"},
    "F": {"S", "E"},
}

START_MAP = {
    frozenset({"N", "S"}): "|",
    frozenset({"E", "W"}): "-",
    frozenset({"N", "E"}): "L",
    frozenset({"N", "W"}): "J",
    frozenset({"S", "W"}): "7",
    frozenset({"S", "E"}): "F",
}


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def in_bounds(y: int, x: int, height: int, width: int) -> bool:
    return 0 <= y < height and 0 <= x < width


def build_grid(lines: Iterable[str]) -> tuple[list[list[str]], tuple[int, int]]:
    grid = [list(line) for line in lines]
    start = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "S":
                start = (y, x)
    if start is None:
        raise ValueError("Start S not found")
    return grid, start


def determine_start_char(grid: list[list[str]], start: tuple[int, int]) -> str:
    height, width = len(grid), len(grid[0])
    y, x = start
    dirs = []
    for direction, (dy, dx) in DIRS.items():
        ny, nx = y + dy, x + dx
        if not in_bounds(ny, nx, height, width):
            continue
        neighbor = grid[ny][nx]
        if neighbor == ".":
            continue
        neighbor_dirs = CONNECTIONS.get(neighbor)
        if neighbor_dirs and OPPOSITE[direction] in neighbor_dirs:
            dirs.append(direction)
    key = frozenset(dirs)
    if key not in START_MAP:
        raise ValueError("Unable to determine start pipe shape")
    return START_MAP[key]


def neighbors(grid: list[list[str]], y: int, x: int) -> Iterable[tuple[int, int]]:
    ch = grid[y][x]
    dirs = CONNECTIONS.get(ch, set())
    height, width = len(grid), len(grid[0])
    for d in dirs:
        dy, dx = DIRS[d]
        ny, nx = y + dy, x + dx
        if not in_bounds(ny, nx, height, width):
            continue
        nch = grid[ny][nx]
        if nch == ".":
            continue
        neighbor_dirs = CONNECTIONS.get(nch, set())
        if OPPOSITE[d] in neighbor_dirs:
            yield ny, nx


def traverse_loop(grid: list[list[str]], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    queue = deque([start])
    distances = {start: 0}
    while queue:
        y, x = queue.popleft()
        for ny, nx in neighbors(grid, y, x):
            if (ny, nx) not in distances:
                distances[(ny, nx)] = distances[(y, x)] + 1
                queue.append((ny, nx))
    return distances


def count_enclosed(grid: list[list[str]], loop_nodes: Set[tuple[int, int]]) -> int:
    total = 0
    height, width = len(grid), len(grid[0])
    for y in range(height):
        inside = False
        pending = None
        for x in range(width):
            if (y, x) not in loop_nodes:
                if inside:
                    total += 1
                continue
            ch = grid[y][x]
            if ch == "|":
                inside = not inside
            elif ch in "LF":
                pending = ch
            elif ch == "7":
                if pending == "L":
                    inside = not inside
                pending = None
            elif ch == "J":
                if pending == "F":
                    inside = not inside
                pending = None
    return total


def solve(lines: Iterable[str]) -> tuple[int, int]:
    grid, start = build_grid(lines)
    start_char = determine_start_char(grid, start)
    sy, sx = start
    grid[sy][sx] = start_char
    distances = traverse_loop(grid, start)
    loop_nodes = set(distances.keys())
    part1_answer = max(distances.values())
    part2_answer = count_enclosed(grid, loop_nodes)
    return part1_answer, part2_answer


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.rstrip("\n") for line in lines]
    return solve(data)[0]


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.rstrip("\n") for line in lines]
    return solve(data)[1]


def run_example() -> None:
    example1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
""".splitlines()
    assert part1(example1) == 4

    example2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".splitlines()
    assert part1(example2) == 8

    example3 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".splitlines()
    assert part2(example3) == 4

    example4 = """\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".splitlines()
    assert part2(example4) == 4

    example5 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".splitlines()
    assert part2(example5) == 8
    print("✓ Example checks passed")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    p1, p2 = solve(read_input())
    print(p1)
    print(p2)

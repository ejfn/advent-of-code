#!/usr/bin/env python3
"""
Advent of Code 2023 Day 18: Lavaduct Lagoon
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


DIRS = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}

DIRS_NUM = {
    0: DIRS["R"],
    1: DIRS["D"],
    2: DIRS["L"],
    3: DIRS["U"],
}


def polygon_area(moves: list[tuple[int, int]]) -> int:
    x, y = 0, 0
    points = [(x, y)]
    perimeter = 0
    for dx, dy, steps in moves:
        x += dx * steps
        y += dy * steps
        points.append((x, y))
        perimeter += steps

    shoelace = 0
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        shoelace += x1 * y2 - x2 * y1
    area = abs(shoelace) // 2
    return area + perimeter // 2 + 1


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    moves = []
    for line in data:
        direction, steps_str, _ = line.split()
        dx, dy = DIRS[direction]
        steps = int(steps_str)
        moves.append((dx, dy, steps))
    return polygon_area(moves)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    moves = []
    for line in data:
        _, _, color = line.split()
        hex_value = color.strip("()#")
        steps = int(hex_value[:5], 16)
        dir_idx = int(hex_value[5])
        dx, dy = DIRS_NUM[dir_idx]
        moves.append((dx, dy, steps))
    return polygon_area(moves)


def run_example() -> None:
    example = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".splitlines()
    assert part1(example) == 62
    assert part2(example) == 952408144115
    print("✓ Example checks passed (Part 1: 62, Part 2: 952408144115)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

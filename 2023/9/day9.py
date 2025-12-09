#!/usr/bin/env python3
"""
Advent of Code 2023 Day 9: Mirage Maintenance
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse(lines: Iterable[str]) -> list[list[int]]:
    return [[int(x) for x in line.split()] for line in lines]


def differences(values: list[int]) -> list[int]:
    return [b - a for a, b in zip(values, values[1:])]


def extrapolate_forward(values: list[int]) -> int:
    if all(v == 0 for v in values):
        return 0
    diff = differences(values)
    return values[-1] + extrapolate_forward(diff)


def extrapolate_backward(values: list[int]) -> int:
    if all(v == 0 for v in values):
        return 0
    diff = differences(values)
    return values[0] - extrapolate_backward(diff)


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    histories = parse(data)
    return sum(extrapolate_forward(history) for history in histories)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    histories = parse(data)
    return sum(extrapolate_backward(history) for history in histories)


def run_example() -> None:
    example = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".splitlines()
    assert part1(example) == 114
    assert part2(example) == 2
    print("✓ Example checks passed (Part 1: 114, Part 2: 2)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

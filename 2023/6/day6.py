#!/usr/bin/env python3
"""
Advent of Code 2023 Day 6: Wait For It
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse(lines: Iterable[str]) -> tuple[list[int], list[int]]:
    data = list(lines)
    times = [int(x) for x in data[0].split()[1:]]
    distances = [int(x) for x in data[1].split()[1:]]
    return times, distances


def ways_for_race(total_time: int, record: int) -> int:
    def distance(hold: int) -> int:
        return hold * (total_time - hold)

    lo, hi = 0, total_time
    while lo < hi:
        mid = (lo + hi) // 2
        if distance(mid) > record:
            hi = mid
        else:
            lo = mid + 1
    first = lo

    lo, hi = 0, total_time
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if distance(mid) > record:
            lo = mid
        else:
            hi = mid - 1
    last = lo

    if first > last:
        return 0
    return last - first + 1


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    times, distances = parse(data)
    result = 1
    for t, d in zip(times, distances):
        result *= ways_for_race(t, d)
    return result


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    time_value = int("".join(data[0].split()[1:]))
    distance_value = int("".join(data[1].split()[1:]))
    return ways_for_race(time_value, distance_value)


def run_example() -> None:
    example = """\
Time:      7  15   30
Distance:  9  40  200
""".splitlines()
    assert part1(example) == 288
    assert part2(example) == 71503
    print("✓ Example checks passed (Part 1: 288, Part 2: 71503)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

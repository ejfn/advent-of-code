#!/usr/bin/env python3
"""
Advent of Code 2023 Day 12: Hot Springs
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    left, right = line.split()
    groups = tuple(int(x) for x in right.split(","))
    return left, groups


def count_arrangements(pattern: str, groups: tuple[int, ...]) -> int:
    @lru_cache(maxsize=None)
    def dp(idx: int, group_idx: int, run_len: int) -> int:
        if idx == len(pattern):
            if run_len > 0:
                if group_idx < len(groups) and run_len == groups[group_idx]:
                    group_idx += 1
                else:
                    return 0
            return 1 if group_idx == len(groups) else 0

        ch = pattern[idx]
        total = 0

        if ch in ".?":
            if run_len > 0:
                if group_idx < len(groups) and run_len == groups[group_idx]:
                    total += dp(idx + 1, group_idx + 1, 0)
            else:
                total += dp(idx + 1, group_idx, 0)

        if ch in "#?":
            if group_idx < len(groups) and run_len + 1 <= groups[group_idx]:
                total += dp(idx + 1, group_idx, run_len + 1)

        return total

    return dp(0, 0, 0)


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    total = 0
    for line in data:
        pattern, groups = parse_line(line)
        total += count_arrangements(pattern, groups)
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    total = 0
    for line in data:
        pattern, groups = parse_line(line)
        expanded_pattern = "?".join([pattern] * 5)
        expanded_groups = groups * 5
        total += count_arrangements(expanded_pattern, expanded_groups)
    return total


def run_example() -> None:
    example = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".splitlines()
    assert part1(example) == 21
    assert part2(example) == 525152
    print("✓ Example checks passed (Part 1: 21, Part 2: 525152)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

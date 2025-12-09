#!/usr/bin/env python3
"""
Advent of Code 2023 Day 4: Scratchcards
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_card(line: str) -> Tuple[int, set[int], list[int]]:
    header, rest = line.split(":")
    card_id = int(header.split()[1])
    winning_str, have_str = rest.split("|")
    winning = {int(x) for x in winning_str.split()}
    have = [int(x) for x in have_str.split()]
    return card_id, winning, have


def count_matches(line: str) -> int:
    _, winning, have = parse_card(line)
    winning_set = winning
    return sum(1 for num in have if num in winning_set)


def part1(lines: Iterable[str] | None = None) -> int:
    data = list(lines) if lines is not None else read_input()
    total = 0
    for line in data:
        matches = count_matches(line)
        if matches:
            total += 1 << (matches - 1)
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    data = list(lines) if lines is not None else read_input()
    copies = [1] * len(data)
    for idx, line in enumerate(data):
        matches = count_matches(line)
        for offset in range(1, matches + 1):
            if idx + offset < len(copies):
                copies[idx + offset] += copies[idx]
    return sum(copies)


def run_example() -> None:
    example = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()
    assert part1(example) == 13
    assert part2(example) == 30
    print("✓ Example checks passed (Part 1: 13, Part 2: 30)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

#!/usr/bin/env python3
"""
Advent of Code 2023 Day 1: Trebuchet?!
"""

from __future__ import annotations

import os
import sys
from typing import Iterable


DIGIT_WORDS = [
    ("zero", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
]


def read_input() -> list[str]:
    """Load puzzle input as a list of lines."""
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def calibration_value(line: str, include_words: bool) -> int:
    """Return calibration value for a single line."""
    digits: list[int] = []
    for idx, ch in enumerate(line):
        if ch.isdigit():
            digits.append(int(ch))
        if include_words:
            for word, value in DIGIT_WORDS:
                if line.startswith(word, idx):
                    digits.append(value)
                    break
    if not digits:
        raise ValueError("Line does not contain any digits")
    return digits[0] * 10 + digits[-1]


def solve(lines: Iterable[str], include_words: bool) -> int:
    total = 0
    for line in lines:
        if not line.strip():
            continue
        total += calibration_value(line, include_words)
    return total


def part1(lines: Iterable[str] | None = None) -> int:
    if lines is None:
        lines = read_input()
    return solve(lines, include_words=False)


def part2(lines: Iterable[str] | None = None) -> int:
    if lines is None:
        lines = read_input()
    return solve(lines, include_words=True)


def run_example() -> None:
    part1_example = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".splitlines()
    part2_example = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".splitlines()

    assert part1(part1_example) == 142
    assert part2(part2_example) == 281
    print("✓ Example checks passed (Part 1: 142, Part 2: 281)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()

    print(part1())
    print(part2())

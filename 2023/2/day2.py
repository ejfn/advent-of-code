#!/usr/bin/env python3
"""
Advent of Code 2023 Day 2: Cube Conundrum
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Iterable


LIMITS = {"red": 12, "green": 13, "blue": 14}


@dataclass(frozen=True)
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_line(line: str) -> tuple[int, list[Draw]]:
    header, rest = line.split(":")
    game_id = int(header.split()[1])

    draws: list[Draw] = []
    for chunk in rest.split(";"):
        counts: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
        for item in chunk.split(","):
            item = item.strip()
            if not item:
                continue
            number_str, color = item.split()
            counts[color] = int(number_str)
        draws.append(Draw(**counts))
    return game_id, draws


def part1(lines: Iterable[str] | None = None) -> int:
    if lines is None:
        lines = read_input()

    total = 0
    for line in lines:
        game_id, draws = parse_line(line)
        if all(draw.red <= LIMITS["red"] and draw.green <= LIMITS["green"] and draw.blue <= LIMITS["blue"] for draw in draws):
            total += game_id
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    if lines is None:
        lines = read_input()

    total = 0
    for line in lines:
        _, draws = parse_line(line)
        max_red = max(draw.red for draw in draws)
        max_green = max(draw.green for draw in draws)
        max_blue = max(draw.blue for draw in draws)
        total += max_red * max_green * max_blue
    return total


def run_example() -> None:
    example = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".splitlines()
    assert part1(example) == 8
    assert part2(example) == 2286
    print("✓ Example checks passed (Part 1: 8, Part 2: 2286)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

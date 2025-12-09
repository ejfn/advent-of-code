#!/usr/bin/env python3
"""
Advent of Code 2023 Day 8: Haunted Wasteland
"""

from __future__ import annotations

import math
import os
import sys
from typing import Dict, Iterable, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse(lines: Iterable[str]) -> tuple[str, Dict[str, tuple[str, str]]]:
    data = list(lines)
    instructions = data[0]
    network: Dict[str, tuple[str, str]] = {}
    for line in data[1:]:
        node, rest = line.split(" = ")
        left, right = rest.strip("()").split(", ")
        network[node] = (left, right)
    return instructions, network


def steps_to_target(start: str, endswith: str, instructions: str, network: dict[str, tuple[str, str]]) -> int:
    idx = 0
    current = start
    steps = 0
    n = len(instructions)
    while not current.endswith(endswith):
        instr = instructions[idx % n]
        left, right = network[current]
        current = left if instr == "L" else right
        idx += 1
        steps += 1
    return steps


def part1(lines: Iterable[str] | None = None) -> int:
    raw = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    instructions, network = parse(raw)
    current = "AAA"
    n = len(instructions)
    steps = 0
    idx = 0
    while current != "ZZZ":
        instr = instructions[idx % n]
        left, right = network[current]
        current = left if instr == "L" else right
        idx += 1
        steps += 1
    return steps


def part2(lines: Iterable[str] | None = None) -> int:
    raw = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    instructions, network = parse(raw)
    starts = [node for node in network if node.endswith("A")]
    lengths = [steps_to_target(start, "Z", instructions, network) for start in starts]
    result = lengths[0]
    for length in lengths[1:]:
        result = math.lcm(result, length)
    return result


def run_example() -> None:
    example1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()
    assert part1(example1) == 2

    example2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()
    assert part1(example2) == 6

    example3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()
    assert part2(example3) == 6
    print("✓ Example checks passed")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

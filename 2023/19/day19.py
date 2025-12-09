#!/usr/bin/env python3
"""
Advent of Code 2023 Day 19: Aplenty
"""

from __future__ import annotations

import os
import sys
from functools import lru_cache
from math import prod
from typing import Dict, Iterable, List, Tuple


def read_input() -> tuple[list[str], list[str]]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        sections = f.read().strip().split("\n\n")
    workflows = sections[0].splitlines()
    parts = sections[1].splitlines()
    return workflows, parts


def parse_workflows(workflow_lines: list[str]) -> dict[str, list[tuple[tuple[str, str, int] | None, str]]]:
    workflows: dict[str, list[tuple[tuple[str, str, int] | None, str]]] = {}
    for line in workflow_lines:
        name, rest = line.split("{")
        rest = rest.rstrip("}")
        rules = []
        for token in rest.split(","):
            if ":" in token:
                cond_str, target = token.split(":")
                if "<" in cond_str:
                    attr, value = cond_str.split("<")
                    rules.append(((attr, "<", int(value)), target))
                else:
                    attr, value = cond_str.split(">")
                    rules.append(((attr, ">", int(value)), target))
            else:
                rules.append((None, token))
        workflows[name] = rules
    return workflows


def parse_part(line: str) -> dict[str, int]:
    line = line.strip("{}")
    values = {}
    for token in line.split(","):
        attr, value = token.split("=")
        values[attr] = int(value)
    return values


def run_workflow(workflows: dict[str, list], part: dict[str, int]) -> bool:
    current = "in"
    while True:
        if current == "A":
            return True
        if current == "R":
            return False
        for cond, target in workflows[current]:
            if cond is None:
                current = target
                break
            attr, op, value = cond
            attr_value = part[attr]
            if op == "<":
                if attr_value < value:
                    current = target
                    break
            else:
                if attr_value > value:
                    current = target
                    break


ATTR_ORDER = ["x", "m", "a", "s"]
ATTR_INDEX = {attr: idx for idx, attr in enumerate(ATTR_ORDER)}


def set_range(ranges: tuple[tuple[int, int], ...], idx: int, new_range: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    lst = list(ranges)
    lst[idx] = new_range
    return tuple(lst)


def part2_count(workflows: dict[str, list[tuple[tuple[str, str, int] | None, str]]]) -> int:
    @lru_cache(maxsize=None)
    def dfs(workflow_name: str, ranges: tuple[tuple[int, int], ...]) -> int:
        if workflow_name == "A":
            return prod(hi - lo + 1 for lo, hi in ranges)
        if workflow_name == "R":
            return 0
        total = 0
        current_ranges = ranges
        for cond, target in workflows[workflow_name]:
            if cond is None:
                total += dfs(target, current_ranges)
                break
            attr, op, value = cond
            idx = ATTR_INDEX[attr]
            lo, hi = current_ranges[idx]
            if op == "<":
                match_hi = min(hi, value - 1)
                if lo <= match_hi:
                    match_ranges = set_range(current_ranges, idx, (lo, match_hi))
                    total += dfs(target, match_ranges)
                lo = max(lo, value)
                if lo > hi:
                    break
                current_ranges = set_range(current_ranges, idx, (lo, hi))
            else:
                match_lo = max(lo, value + 1)
                if match_lo <= hi:
                    match_ranges = set_range(current_ranges, idx, (match_lo, hi))
                    total += dfs(target, match_ranges)
                hi = min(hi, value)
                if lo > hi:
                    break
                current_ranges = set_range(current_ranges, idx, (lo, hi))
        return total

    initial_ranges = tuple((1, 4000) for _ in ATTR_ORDER)
    return dfs("in", initial_ranges)


def part1(lines: Iterable[str] | None = None) -> int:
    workflows_raw, parts_raw = read_input()
    workflows = parse_workflows(workflows_raw)
    total = 0
    for part_line in parts_raw:
        part = parse_part(part_line)
        if run_workflow(workflows, part):
            total += sum(part[attr] for attr in ATTR_ORDER)
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    workflows_raw, parts_raw = read_input()
    workflows = parse_workflows(workflows_raw)
    return part2_count(workflows)


def run_example() -> None:
    example = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines()
    workflows_raw = example[:11]
    parts_raw = example[12:]
    workflows = parse_workflows(workflows_raw)
    total = 0
    for part_line in parts_raw:
        part = parse_part(part_line)
        if run_workflow(workflows, part):
            total += sum(part[attr] for attr in ATTR_ORDER)
    assert total == 19114
    assert part2_count(workflows) == 167409079868000
    print("✓ Example checks passed (Part 1: 19114, Part 2: 167409079868000)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

#!/usr/bin/env python3
"""
Advent of Code 2023 Day 22: Sand Slabs
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict, deque
from typing import Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_bricks(lines: list[str]) -> list[tuple[int, int, int, int, int, int]]:
    bricks = []
    for idx, line in enumerate(lines):
        left, right = line.split("~")
        x1, y1, z1 = map(int, left.split(","))
        x2, y2, z2 = map(int, right.split(","))
        bricks.append((min(x1, x2), min(y1, y2), min(z1, z2), max(x1, x2), max(y1, y2), max(z1, z2)))
    return bricks


def settle_bricks(bricks: list[tuple[int, int, int, int, int, int]]):
    bricks_with_id = sorted(list(enumerate(bricks)), key=lambda item: item[1][2])
    column_top: dict[tuple[int, int], tuple[int, int]] = {}  # (x,y) -> (top_z, brick_id)
    settled = {}
    supported_by = defaultdict(set)
    supports = defaultdict(set)

    for brick_id, (x1, y1, z1, x2, y2, z2) in bricks_with_id:
        max_support_z = 0
        supporters = set()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                top_info = column_top.get((x, y))
                if top_info:
                    top_z, supporter_id = top_info
                    if top_z > max_support_z:
                        max_support_z = top_z
                        supporters = {supporter_id}
                    elif top_z == max_support_z:
                        supporters.add(supporter_id)
        new_base_z = max_support_z + 1
        height = z2 - z1
        new_top_z = new_base_z + height
        settled[brick_id] = (x1, y1, new_base_z, x2, y2, new_top_z)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                column_top[(x, y)] = (new_top_z, brick_id)
        supporters.discard(None)
        supported_by[brick_id] = set(supporters)
        for supporter in supporters:
            supports[supporter].add(brick_id)

    # ensure every brick in dicts
    for brick_id, _ in bricks_with_id:
        supports.setdefault(brick_id, set())
        supported_by.setdefault(brick_id, set())

    return settled, supports, supported_by


def count_safe_bricks(supports: dict[int, set[int]], supported_by: dict[int, set[int]]) -> int:
    safe = 0
    for brick in supports:
        removable = True
        for child in supports[brick]:
            if len(supported_by[child]) == 1:
                removable = False
                break
        if removable:
            safe += 1
    return safe


def chain_reaction(brick: int, supports: dict[int, set[int]], supported_by: dict[int, set[int]]) -> int:
    removed = set([brick])
    queue = deque()
    for child in supports[brick]:
        if supported_by[child] <= removed:
            queue.append(child)

    fallen = 0
    while queue:
        b = queue.popleft()
        if b in removed:
            continue
        removed.add(b)
        fallen += 1
        for child in supports[b]:
            if child not in removed and supported_by[child] <= removed:
                queue.append(child)
    return fallen


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    bricks = parse_bricks(data)
    _, supports, supported_by = settle_bricks(bricks)
    return count_safe_bricks(supports, supported_by)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    bricks = parse_bricks(data)
    _, supports, supported_by = settle_bricks(bricks)
    total = 0
    for brick in supports:
        total += chain_reaction(brick, supports, supported_by)
    return total


def run_example() -> None:
    example = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".splitlines()
    assert part1(example) == 5
    assert part2(example) == 7
    print("✓ Example checks passed (Part 1: 5, Part 2: 7)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

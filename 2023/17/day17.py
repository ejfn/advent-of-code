#!/usr/bin/env python3
"""
Advent of Code 2023 Day 17: Clumsy Crucible
"""

from __future__ import annotations

import os
import sys
import heapq
from typing import Dict, Iterable, List, Optional, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


Grid = list[str]
State = tuple[int, int, Optional[int], int]  # row, col, direction index, run length

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def dijkstra(grid: Grid, min_run_before_turn: int, max_run: int, min_run_to_finish: int) -> int:
    rows = len(grid)
    cols = len(grid[0])
    target = (rows - 1, cols - 1)

    pq: list[tuple[int, State]] = []
    dist: Dict[State, int] = {}

    # start with no direction
    heapq.heappush(pq, (0, (0, 0, None, 0)))
    dist[(0, 0, None, 0)] = 0

    while pq:
        cost, (r, c, dir_idx, run_len) = heapq.heappop(pq)
        if (r, c) == target:
            if dir_idx is None:
                return cost
            if run_len >= min_run_to_finish:
                return cost
        if cost != dist[(r, c, dir_idx, run_len)]:
            continue

        for new_dir_idx, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if dir_idx is not None and (new_dir_idx + 2) % 4 == dir_idx:
                continue

            if dir_idx is None:
                new_run = 1
            elif new_dir_idx == dir_idx:
                if run_len >= max_run:
                    continue
                new_run = run_len + 1
            else:
                if run_len < min_run_before_turn:
                    continue
                new_run = 1

            new_cost = cost + int(grid[nr][nc])
            state = (nr, nc, new_dir_idx, new_run)
            if state not in dist or new_cost < dist[state]:
                dist[state] = new_cost
                heapq.heappush(pq, (new_cost, state))

    raise RuntimeError("Target not reachable")


def part1(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    return dijkstra(grid, min_run_before_turn=0, max_run=3, min_run_to_finish=0)


def part2(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    return dijkstra(grid, min_run_before_turn=4, max_run=10, min_run_to_finish=4)


def run_example() -> None:
    example = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".splitlines()
    assert part1(example) == 102
    assert part2(example) == 94
    print("✓ Example checks passed (Part 1: 102, Part 2: 94)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

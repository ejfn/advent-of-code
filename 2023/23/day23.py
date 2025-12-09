#!/usr/bin/env python3
"""
Advent of Code 2023 Day 23: A Long Walk
"""

from __future__ import annotations

import os
import sys
from typing import Dict, Iterable, List, Set, Tuple

sys.setrecursionlimit(1_000_000)


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip("\n") for line in f if line.strip("\n")]


DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

ALL_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_start_end(grid: list[str]) -> tuple[tuple[int, int], tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])
    start = (0, grid[0].index("."))
    end = (rows - 1, grid[-1].index("."))
    return start, end


def part1(lines: Iterable[str] | None = None) -> int:
    grid = read_input() if lines is None else [line.rstrip("\n") for line in lines if line.strip("\n")]
    rows = len(grid)
    cols = len(grid[0])
    start, end = find_start_end(grid)

    best = 0
    visited = set()

    def dfs(r: int, c: int, steps: int) -> None:
        nonlocal best
        if (r, c) == end:
            best = max(best, steps)
            return
        visited.add((r, c))
        current_char = grid[r][c]
        dirs = ALL_DIRS
        if current_char in DIRECTIONS:
            dirs = [DIRECTIONS[current_char]]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue
            if (nr, nc) in visited:
                continue
            dest_char = grid[nr][nc]
            if dest_char in DIRECTIONS:
                if (dr, dc) != DIRECTIONS[dest_char]:
                    continue
            dfs(nr, nc, steps + 1)
        visited.remove((r, c))

    dfs(*start, 0)
    return best


def build_graph(grid: list[str]) -> tuple[dict[tuple[int, int], list[tuple[tuple[int, int], int]]], tuple[int, int], tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])
    start, end = find_start_end(grid)

    def neighbors(r: int, c: int) -> list[tuple[int, int]]:
        result = []
        for dr, dc in ALL_DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                result.append((nr, nc))
        return result

    nodes = {start, end}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue
            neigh = neighbors(r, c)
            if len(neigh) != 2:
                nodes.add((r, c))

    graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = {node: [] for node in nodes}

    for node in nodes:
        for nr, nc in neighbors(*node):
            prev = node
            current = (nr, nc)
            distance = 1
            while current not in nodes:
                next_steps = [n for n in neighbors(*current) if n != prev]
                if not next_steps:
                    break
                prev = current
                current = next_steps[0]
                distance += 1
            graph[node].append((current, distance))
    return graph, start, end


def part2(lines: Iterable[str] | None = None) -> int:
    raw = read_input() if lines is None else [line.rstrip("\n") for line in lines if line.strip("\n")]
    # Convert slopes to open tiles
    grid = []
    for row in raw:
        grid.append(row.replace("^", ".").replace("v", ".").replace("<", ".").replace(">", "."))
    graph, start, end = build_graph(grid)

    best = 0
    visited = set([start])

    def dfs(node: tuple[int, int], distance: int):
        nonlocal best
        if node == end:
            best = max(best, distance)
            return
        for neighbor, cost in graph[node]:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            dfs(neighbor, distance + cost)
            visited.remove(neighbor)

    dfs(start, 0)
    return best


def run_example() -> None:
    example = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
""".splitlines()
    assert part1(example) == 94
    assert part2(example) == 154
    print("✓ Example checks passed (Part 1: 94, Part 2: 154)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

#!/usr/bin/env python3
"""
Advent of Code 2023 Day 25: Snowverload
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Tuple

import networkx as nx


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_graph(lines: list[str]) -> nx.Graph:
    G = nx.Graph()
    for line in lines:
        left, right = line.split(":")
        src = left.strip()
        for dst in right.strip().split():
            G.add_edge(src, dst)
    return G


def count_connected(graph: dict[str, set[str]], start: str, blocked_edges: set[tuple[str, str]]) -> int:
    stack = [start]
    visited = set([start])
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            edge = tuple(sorted((node, neighbor)))
            if edge in blocked_edges:
                continue
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return len(visited)


def part1(lines: Iterable[str] | None = None) -> int:
    G = build_graph(read_input() if lines is None else [line.strip() for line in lines if line.strip()])
    cut_value, (set_a, set_b) = nx.stoer_wagner(G)
    assert cut_value == 3
    return len(set_a) * len(set_b)


if __name__ == "__main__":
    print(part1())

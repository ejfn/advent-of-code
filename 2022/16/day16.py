import functools
import os
import re
import sys
from collections import deque
from textwrap import dedent


def parse(data: str):
    rates = {}
    graph = {}
    pattern = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    )
    for line in data.strip().splitlines():
        match = pattern.match(line)
        valve, rate, targets = match.groups()
        rates[valve] = int(rate)
        graph[valve] = [target.strip() for target in targets.split(",")]
    return rates, graph


def shortest_paths(graph):
    dists = {}
    for src in graph:
        queue = deque([(src, 0)])
        visited = {src}
        dists[src] = {}
        while queue:
            node, dist = queue.popleft()
            dists[src][node] = dist
            for neigh in graph[node]:
                if neigh not in visited:
                    visited.add(neigh)
                    queue.append((neigh, dist + 1))
    return dists


def build_useful(rates, dists):
    useful = [valve for valve, rate in rates.items() if rate > 0]
    return useful


def solve_single(rates, dists, useful, total_time):
    index = {valve: idx for idx, valve in enumerate(useful)}

    @functools.lru_cache(maxsize=None)
    def dfs(current: str, time_left: int, opened_mask: int) -> int:
        best = 0
        for valve in useful:
            bit = 1 << index[valve]
            if opened_mask & bit:
                continue
            dist = dists[current][valve]
            remaining = time_left - dist - 1
            if remaining <= 0:
                continue
            released = rates[valve] * remaining + dfs(
                valve, remaining, opened_mask | bit
            )
            best = max(best, released)
        return best

    best_by_mask = {}

    def record(current: str, time_left: int, opened_mask: int, accumulated: int):
        best_by_mask[opened_mask] = max(best_by_mask.get(opened_mask, 0), accumulated)
        for valve in useful:
            bit = 1 << index[valve]
            if opened_mask & bit:
                continue
            dist = dists[current][valve]
            remaining = time_left - dist - 1
            if remaining <= 0:
                continue
            gain = rates[valve] * remaining
            record(valve, remaining, opened_mask | bit, accumulated + gain)

    record("AA", total_time, 0, 0)
    return dfs("AA", total_time, 0), best_by_mask, len(useful)


def part1(data: str) -> int:
    rates, graph = parse(data)
    dists = shortest_paths(graph)
    useful = build_useful(rates, dists)
    best, _, _ = solve_single(rates, dists, useful, total_time=30)
    return best


def part2(data: str) -> int:
    rates, graph = parse(data)
    dists = shortest_paths(graph)
    useful = build_useful(rates, dists)
    _, best_by_mask, n = solve_single(rates, dists, useful, total_time=26)
    size = 1 << n
    best_subset = [0] * size
    for mask, score in best_by_mask.items():
        best_subset[mask] = max(best_subset[mask], score)
    for bit in range(n):
        for mask in range(size):
            if mask & (1 << bit):
                best_subset[mask] = max(best_subset[mask], best_subset[mask ^ (1 << bit)])
    all_mask = size - 1
    answer = 0
    for mask in range(size):
        answer = max(answer, best_subset[mask] + best_subset[all_mask ^ mask])
    return answer


def run_example() -> None:
    example = dedent(
        """\
        Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        Valve BB has flow rate=13; tunnels lead to valves CC, AA
        Valve CC has flow rate=2; tunnels lead to valves DD, BB
        Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
        Valve EE has flow rate=3; tunnels lead to valves FF, DD
        Valve FF has flow rate=0; tunnels lead to valves EE, GG
        Valve GG has flow rate=0; tunnels lead to valves FF, HH
        Valve HH has flow rate=22; tunnel leads to valve GG
        Valve II has flow rate=0; tunnels lead to valves AA, JJ
        Valve JJ has flow rate=21; tunnel leads to valve II
        """
    )
    assert part1(example) == 1651
    assert part2(example) == 1707
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

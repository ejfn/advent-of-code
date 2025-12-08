import os
import sys
from collections import defaultdict


def parse_input(filename):
    """Return an adjacency map for the undirected LAN graph."""
    graph = defaultdict(set)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            a, b = line.split("-")
            graph[a].add(b)
            graph[b].add(a)
    return graph


def count_t_triangles(graph):
    """Part 1: count triangles with at least one name starting with 't'."""
    total = 0
    nodes = sorted(graph)
    for i, a in enumerate(nodes):
        neighbors_a = [n for n in graph[a] if n > a]
        for b in neighbors_a:
            common = graph[a] & graph[b]
            for c in (n for n in common if n > b):
                if any(name.startswith("t") for name in (a, b, c)):
                    total += 1
    return total


def bron_kerbosch(graph, r, p, x, best):
    """Bron–Kerbosch with pivoting; updates best clique in place."""
    if not p and not x:
        if len(r) > len(best[0]):
            best[0] = tuple(sorted(r))
        return

    pivot = None
    if p or x:
        pivot = max(p | x, key=lambda node: len(graph[node]))

    nodes_to_iterate = p - graph[pivot] if pivot is not None else set(p)
    for v in list(nodes_to_iterate):
        bron_kerbosch(
            graph,
            r | {v},
            p & graph[v],
            x & graph[v],
            best,
        )
        p.remove(v)
        x.add(v)


def find_largest_clique(graph):
    """Part 2: return comma-joined sorted names of largest clique."""
    p = set(graph.keys())
    best = [()]
    bron_kerbosch(graph, set(), p, set(), best)
    return ",".join(best[0])


def part1():
    input_file = os.path.join(sys.path[0], "input.txt")
    graph = parse_input(input_file)
    return count_t_triangles(graph)


def part2():
    input_file = os.path.join(sys.path[0], "input.txt")
    graph = parse_input(input_file)
    return find_largest_clique(graph)


def run_example():
    data = """\
ta-tb
tb-tc
tc-ta
aa-ta
aa-tb
aa-tc
"""
    tmp = "/tmp/aoc2024_day23_example.txt"
    with open(tmp, "w") as f:
        f.write(data)
    graph = parse_input(tmp)
    print("Example part 1:", count_t_triangles(graph))  # 4 triangles
    print("Example part 2:", find_largest_clique(graph))  # clique of size 4


if __name__ == "__main__":
    print("=== Example ===")
    run_example()

    input_file = os.path.join(sys.path[0], "input.txt")
    if os.path.exists(input_file):
        print("\n=== Part 1 ===")
        print(part1())

        print("\n=== Part 2 ===")
        print(part2())
    else:
        print(
            "\nNo input.txt found in this directory. Add your puzzle input to run part 1 and part 2."
        )

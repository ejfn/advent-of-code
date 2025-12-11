import os
import sys
from functools import cache

def parse_input(lines):
    """Parse input into adjacency list (dict of node -> list of neighbors)."""
    graph = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split(': ')
        node = parts[0]
        if len(parts) > 1:
            neighbors = parts[1].split()
        else:
            neighbors = []
        graph[node] = neighbors
    return graph

def count_paths(graph, start, end):
    """Count all paths from start to end using memoization."""
    @cache
    def dfs(node):
        if node == end:
            return 1
        if node not in graph:
            return 0
        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor)
        return total

    return dfs(start)

def run_example():
    """Test with the example from the puzzle."""
    example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

    lines = example.strip().split('\n')
    graph = parse_input(lines)
    print("Example graph:", graph)

    result = count_paths(graph, 'you', 'out')
    print(f"Example result: {result} (expected: 5)")
    return result

def part1():
    """Find number of paths from 'you' to 'out'."""
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')

    graph = parse_input(lines)
    result = count_paths(graph, 'you', 'out')
    return result

def part2():
    """Part 2 - to be implemented after reading updated puzzle."""
    pass

if __name__ == "__main__":
    print("=== Example ===")
    run_example()
    print()

    print("=== Part 1 ===")
    result1 = part1()
    print(f"Part 1: {result1}")

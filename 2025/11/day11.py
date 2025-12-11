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

def count_paths_with_required(graph, start, end, required):
    """Count paths from start to end that visit all required nodes.

    required: frozenset of nodes that must be visited
    """
    @cache
    def dfs(node, visited_required):
        # Update visited_required if current node is in required set
        if node in required:
            visited_required = visited_required | frozenset([node])

        if node == end:
            # Only count if all required nodes were visited
            if visited_required == required:
                return 1
            return 0

        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor, visited_required)
        return total

    return dfs(start, frozenset())

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

def run_example_part2():
    """Test Part 2 with the example from the puzzle."""
    example = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

    lines = example.strip().split('\n')
    graph = parse_input(lines)

    # Count paths that visit both dac and fft
    required = frozenset(['dac', 'fft'])
    result = count_paths_with_required(graph, 'svr', 'out', required)
    print(f"Example Part 2 result: {result} (expected: 2)")
    return result

def part1():
    """Find number of paths from 'you' to 'out'."""
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')

    graph = parse_input(lines)
    result = count_paths(graph, 'you', 'out')
    return result

def part2():
    """Find paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')

    graph = parse_input(lines)
    required = frozenset(['dac', 'fft'])
    result = count_paths_with_required(graph, 'svr', 'out', required)
    return result

if __name__ == "__main__":
    print("=== Example ===")
    run_example()
    print()

    print("=== Example Part 2 ===")
    run_example_part2()
    print()

    print("=== Part 1 ===")
    result1 = part1()
    print(f"Part 1: {result1}")

    print()
    print("=== Part 2 ===")
    result2 = part2()
    print(f"Part 2: {result2}")

import os
import sys
from collections import deque


def parse_input(text):
    """Parse input into adjacency dict."""
    graph = {}
    for line in text.strip().split('\n'):
        parts = line.split(' <-> ')
        node = int(parts[0])
        neighbors = [int(x.strip()) for x in parts[1].split(',')]
        graph[node] = neighbors
    return graph


def bfs_group(graph, start):
    """Find all nodes in the connected component containing start."""
    visited = set()
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append(neighbor)
    
    return visited


def part1(graph):
    """Count programs in the group containing program 0."""
    return len(bfs_group(graph, 0))


def part2(graph):
    """Count total number of groups."""
    remaining = set(graph.keys())
    groups = 0
    
    while remaining:
        start = next(iter(remaining))
        group = bfs_group(graph, start)
        remaining -= group
        groups += 1
    
    return groups


def run_example():
    example = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    graph = parse_input(example)
    assert part1(graph) == 6
    print("Part 1 example passed!")
    assert part2(graph) == 2
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        graph = parse_input(f.read())
    
    print(f"Part 1: {part1(graph)}")
    print(f"Part 2: {part2(graph)}")

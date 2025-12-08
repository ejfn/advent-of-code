import os
import sys
from collections import deque

def parse_input(filename):
    """Parse the input file to get list of falling byte coordinates."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    coordinates = []
    for line in lines:
        x, y = map(int, line.split(','))
        coordinates.append((x, y))
    return coordinates

def find_shortest_path(corrupted, grid_size):
    """Find shortest path from (0,0) to (grid_size, grid_size) using BFS."""
    start = (0, 0)
    end = (grid_size, grid_size)

    # BFS
    queue = deque([(start, 0)])  # (position, steps)
    visited = {start}

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check bounds
            if 0 <= nx <= grid_size and 0 <= ny <= grid_size:
                # Check not corrupted and not visited
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))

    return -1  # No path found

def find_first_blocking_byte(coordinates, grid_size):
    """Find the first byte that blocks the path using binary search."""
    # Binary search to find the first blocking byte
    left = 0
    right = len(coordinates) - 1
    result = None

    while left <= right:
        mid = (left + right) // 2

        # Check if path exists with first mid+1 bytes fallen
        corrupted = set(coordinates[:mid + 1])
        path_exists = find_shortest_path(corrupted, grid_size) != -1

        if path_exists:
            # Path still exists, need to drop more bytes
            left = mid + 1
        else:
            # Path is blocked, this might be our answer
            result = coordinates[mid]
            # But check if we can find an earlier blocking byte
            right = mid - 1

    return result

def run_example():
    """Test with the example from the puzzle."""
    example_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    lines = [line.strip() for line in example_input.split('\n') if line.strip()]
    coordinates = []
    for line in lines:
        x, y = map(int, line.split(','))
        coordinates.append((x, y))

    # Part 1: Take first 12 bytes for the example
    corrupted = set(coordinates[:12])

    print("Example Part 1: First 12 bytes fallen")
    print(f"Corrupted coordinates: {corrupted}")

    # Find shortest path on 7x7 grid (0-6)
    result = find_shortest_path(corrupted, 6)
    print(f"Shortest path: {result} steps")
    print(f"Expected: 22 steps")
    print()

    # Part 2: Find first blocking byte
    print("Example Part 2: Finding first blocking byte")
    blocking_byte = find_first_blocking_byte(coordinates, 6)
    print(f"First blocking byte: {blocking_byte}")
    print(f"Expected: 6,1")
    print()

def part1():
    """Solve Part 1: Find shortest path after 1024 bytes have fallen."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    coordinates = parse_input(input_file)

    # Take first 1024 bytes
    corrupted = set(coordinates[:1024])

    # Find shortest path on 71x71 grid (0-70)
    result = find_shortest_path(corrupted, 70)

    return result

def part2():
    """Solve Part 2: Find first byte that blocks the path."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    coordinates = parse_input(input_file)

    # Find the first blocking byte
    blocking_byte = find_first_blocking_byte(coordinates, 70)

    return blocking_byte

if __name__ == "__main__":
    print("=== Testing Example ===")
    run_example()

    print("=== Part 1 ===")
    result1 = part1()
    print(f"Minimum steps to reach exit: {result1}")

    print("\n=== Part 2 ===")
    result2 = part2()
    print(f"First blocking byte: {result2[0]},{result2[1]}")

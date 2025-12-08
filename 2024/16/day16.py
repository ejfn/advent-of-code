import os
import sys
import heapq
from collections import defaultdict

def parse_input(filename):
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    grid = []
    start = None
    end = None

    for r, line in enumerate(lines):
        row = []
        for c, ch in enumerate(line):
            if ch == 'S':
                start = (r, c)
                row.append('.')
            elif ch == 'E':
                end = (r, c)
                row.append('.')
            else:
                row.append(ch)
        grid.append(row)

    return grid, start, end

def part1():
    filename = os.path.join(sys.path[0], 'input.txt')
    grid, start, end = parse_input(filename)

    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # State: (cost, row, col, direction)
    # Start facing East (direction 0)
    pq = [(0, start[0], start[1], 0)]
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            return cost

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))

        # Try rotating clockwise
        new_d = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

        # Try rotating counter-clockwise
        new_d = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

    return -1

def part2():
    filename = os.path.join(sys.path[0], 'input.txt')
    grid, start, end = parse_input(filename)

    # TODO: Implement Part 2
    return 0

def run_example():
    example1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

    lines = example1.strip().split('\n')
    grid = []
    start = None
    end = None

    for r, line in enumerate(lines):
        row = []
        for c, ch in enumerate(line):
            if ch == 'S':
                start = (r, c)
                row.append('.')
            elif ch == 'E':
                end = (r, c)
                row.append('.')
            else:
                row.append(ch)
        grid.append(row)

    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Start: {start}, End: {end}")

    # Run pathfinding
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(0, start[0], start[1], 0)]
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            print(f"Example 1 result: {cost} (expected 7036)")
            break

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))

        # Try rotating clockwise
        new_d = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

        # Try rotating counter-clockwise
        new_d = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

    # Test example 2
    example2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

    lines = example2.strip().split('\n')
    grid = []
    start = None
    end = None

    for r, line in enumerate(lines):
        row = []
        for c, ch in enumerate(line):
            if ch == 'S':
                start = (r, c)
                row.append('.')
            elif ch == 'E':
                end = (r, c)
                row.append('.')
            else:
                row.append(ch)
        grid.append(row)

    print(f"\nGrid size: {len(grid)}x{len(grid[0])}")
    print(f"Start: {start}, End: {end}")

    pq = [(0, start[0], start[1], 0)]
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            print(f"Example 2 result: {cost} (expected 11048)")
            break

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))

        # Try rotating clockwise
        new_d = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

        # Try rotating counter-clockwise
        new_d = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

if __name__ == "__main__":
    print("Testing examples...")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())

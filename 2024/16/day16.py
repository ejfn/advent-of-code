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

    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Run Dijkstra and track costs and predecessors
    pq = [(0, start[0], start[1], 0)]
    costs = {}  # (r, c, d) -> min cost to reach this state
    predecessors = defaultdict(list)  # (r, c, d) -> list of predecessor states

    min_end_cost = float('inf')
    end_states = []

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        # If we've found the end, track it
        if (r, c) == end:
            if cost < min_end_cost:
                min_end_cost = cost
                end_states = [(r, c, d)]
            elif cost == min_end_cost:
                end_states.append((r, c, d))

        # Skip if we've seen this state with a better cost
        if (r, c, d) in costs and costs[(r, c, d)] < cost:
            continue

        # Record this cost
        if (r, c, d) not in costs:
            costs[(r, c, d)] = cost

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            new_cost = cost + 1
            new_state = (nr, nc, d)

            if new_state not in costs or costs[new_state] >= new_cost:
                if new_state not in costs or costs[new_state] > new_cost:
                    costs[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, nr, nc, d))
                    predecessors[new_state] = [(r, c, d)]
                elif costs[new_state] == new_cost:
                    predecessors[new_state].append((r, c, d))

        # Try rotating clockwise
        new_d = (d + 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, new_d)

        if new_state not in costs or costs[new_state] >= new_cost:
            if new_state not in costs or costs[new_state] > new_cost:
                costs[new_state] = new_cost
                heapq.heappush(pq, (new_cost, r, c, new_d))
                predecessors[new_state] = [(r, c, d)]
            elif costs[new_state] == new_cost:
                predecessors[new_state].append((r, c, d))

        # Try rotating counter-clockwise
        new_d = (d - 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, new_d)

        if new_state not in costs or costs[new_state] >= new_cost:
            if new_state not in costs or costs[new_state] > new_cost:
                costs[new_state] = new_cost
                heapq.heappush(pq, (new_cost, r, c, new_d))
                predecessors[new_state] = [(r, c, d)]
            elif costs[new_state] == new_cost:
                predecessors[new_state].append((r, c, d))

    # Backtrack from all optimal end states to find all tiles on optimal paths
    tiles_on_path = set()
    queue = end_states[:]
    visited_states = set(end_states)

    while queue:
        state = queue.pop()
        r, c, d = state
        tiles_on_path.add((r, c))

        for pred in predecessors[state]:
            if pred not in visited_states:
                visited_states.add(pred)
                queue.append(pred)

    return len(tiles_on_path)

def run_example():
    # Test Part 1
    print("Part 1 Examples:")
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

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(0, start[0], start[1], 0)]
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            print(f"Example 1: {cost} (expected 7036)")
            break

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))

        new_d = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

        new_d = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

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

    pq = [(0, start[0], start[1], 0)]
    visited = set()

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        if (r, c) == end:
            print(f"Example 2: {cost} (expected 11048)")
            break

        if (r, c, d) in visited:
            continue
        visited.add((r, c, d))

        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))

        new_d = (d + 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

        new_d = (d - 1) % 4
        heapq.heappush(pq, (cost + 1000, r, c, new_d))

    # Test Part 2 - helper function to count tiles
    def count_tiles(example_str):
        lines = example_str.strip().split('\n')
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

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        pq = [(0, start[0], start[1], 0)]
        costs = {}
        predecessors = defaultdict(list)
        min_end_cost = float('inf')
        end_states = []

        while pq:
            cost, r, c, d = heapq.heappop(pq)

            if (r, c) == end:
                if cost < min_end_cost:
                    min_end_cost = cost
                    end_states = [(r, c, d)]
                elif cost == min_end_cost:
                    end_states.append((r, c, d))

            if (r, c, d) in costs and costs[(r, c, d)] < cost:
                continue

            if (r, c, d) not in costs:
                costs[(r, c, d)] = cost

            dr, dc = directions[d]
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
                new_cost = cost + 1
                new_state = (nr, nc, d)

                if new_state not in costs or costs[new_state] >= new_cost:
                    if new_state not in costs or costs[new_state] > new_cost:
                        costs[new_state] = new_cost
                        heapq.heappush(pq, (new_cost, nr, nc, d))
                        predecessors[new_state] = [(r, c, d)]
                    elif costs[new_state] == new_cost:
                        predecessors[new_state].append((r, c, d))

            new_d = (d + 1) % 4
            new_cost = cost + 1000
            new_state = (r, c, new_d)

            if new_state not in costs or costs[new_state] >= new_cost:
                if new_state not in costs or costs[new_state] > new_cost:
                    costs[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, r, c, new_d))
                    predecessors[new_state] = [(r, c, d)]
                elif costs[new_state] == new_cost:
                    predecessors[new_state].append((r, c, d))

            new_d = (d - 1) % 4
            new_cost = cost + 1000
            new_state = (r, c, new_d)

            if new_state not in costs or costs[new_state] >= new_cost:
                if new_state not in costs or costs[new_state] > new_cost:
                    costs[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, r, c, new_d))
                    predecessors[new_state] = [(r, c, d)]
                elif costs[new_state] == new_cost:
                    predecessors[new_state].append((r, c, d))

        tiles_on_path = set()
        queue = end_states[:]
        visited_states = set(end_states)

        while queue:
            state = queue.pop()
            r, c, d = state
            tiles_on_path.add((r, c))

            for pred in predecessors[state]:
                if pred not in visited_states:
                    visited_states.add(pred)
                    queue.append(pred)

        return len(tiles_on_path)

    print("\nPart 2 Examples:")
    print(f"Example 1: {count_tiles(example1)} (expected 45)")
    print(f"Example 2: {count_tiles(example2)} (expected 64)")

if __name__ == "__main__":
    print("Testing examples...")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())

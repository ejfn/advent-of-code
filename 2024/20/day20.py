import os
import sys
from collections import deque


def parse_input(filename):
    """Parse the grid and locate the start and end positions."""
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    grid = [list(line) for line in lines]
    start = end = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
                grid[r][c] = "."
            elif ch == "E":
                end = (r, c)
                grid[r][c] = "."

    if start is None or end is None:
        raise ValueError("Grid must contain both S and E")

    return grid, start, end


def bfs(grid, start):
    """Return shortest distances from start to all open cells."""
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                if (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))
    return dist


def count_cheats(grid, start, end, cheat_range, threshold=100):
    """Count cheats that save at least `threshold` picoseconds."""
    dist_start = bfs(grid, start)
    dist_end = bfs(grid, end)
    baseline = dist_start[end]

    rows, cols = len(grid), len(grid[0])
    count = 0

    for (r, c), d0 in dist_start.items():
        for dr in range(-cheat_range, cheat_range + 1):
            remaining = cheat_range - abs(dr)
            for dc in range(-remaining, remaining + 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if grid[nr][nc] == "#":
                    continue
                if (nr, nc) not in dist_end:
                    continue
                cheat_cost = abs(dr) + abs(dc)
                total = d0 + cheat_cost + dist_end[(nr, nc)]
                if baseline - total >= threshold:
                    count += 1

    return count


def part1():
    input_file = os.path.join(sys.path[0], "input.txt")
    grid, start, end = parse_input(input_file)
    return count_cheats(grid, start, end, cheat_range=2, threshold=100)


def part2():
    input_file = os.path.join(sys.path[0], "input.txt")
    grid, start, end = parse_input(input_file)
    return count_cheats(grid, start, end, cheat_range=20, threshold=100)


def run_example():
    """Self-contained example to illustrate cheat counting."""
    example = """#########
#S....#E#
#.###.#.#
#...#...#
#########"""

    tmp_path = "/tmp/aoc2024_day20_example.txt"
    with open(tmp_path, "w") as f:
        f.write(example)

    grid, start, end = parse_input(tmp_path)
    dist_start = bfs(grid, start)
    baseline = dist_start[end]
    p1 = count_cheats(grid, start, end, cheat_range=2, threshold=1)
    p2 = count_cheats(grid, start, end, cheat_range=4, threshold=1)

    print("Example baseline time:", baseline)
    print("Cheats (range 2, save >=1):", p1)
    print("Cheats (range 4, save >=1):", p2)


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
        print("\nNo input.txt found in this directory. Add your puzzle input to run part 1 and part 2.")

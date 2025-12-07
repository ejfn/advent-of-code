import os
import sys
from collections import deque

def load_input():
    """Load the topographic map from input.txt"""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    return [[int(c) for c in line] for line in lines]

def find_trailheads(grid):
    """Find all positions with height 0"""
    trailheads = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                trailheads.append((r, c))
    return trailheads

def get_neighbors(r, c, rows, cols):
    """Get valid neighboring positions (up, down, left, right)"""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def calculate_trailhead_score(grid, start_r, start_c):
    """
    Calculate the score of a trailhead (number of 9-height positions reachable
    via a valid hiking trail from this trailhead)
    """
    rows, cols = len(grid), len(grid[0])
    reachable_nines = set()

    # BFS to find all reachable 9s
    queue = deque([(start_r, start_c)])
    visited = {(start_r, start_c)}

    while queue:
        r, c = queue.popleft()
        current_height = grid[r][c]

        # If we reached a 9, add it to our set
        if current_height == 9:
            reachable_nines.add((r, c))
            continue

        # Explore neighbors that are exactly 1 higher
        for nr, nc in get_neighbors(r, c, rows, cols):
            if (nr, nc) not in visited and grid[nr][nc] == current_height + 1:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(reachable_nines)

def part1():
    """Calculate sum of scores of all trailheads"""
    grid = load_input()
    trailheads = find_trailheads(grid)

    total_score = 0
    for r, c in trailheads:
        score = calculate_trailhead_score(grid, r, c)
        total_score += score

    return total_score

def part2():
    """Part 2 solution (to be implemented)"""
    return 0

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

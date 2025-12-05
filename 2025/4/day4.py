import os
import sys

# Load input from input.txt in same directory as script
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    grid = [line.strip() for line in f.readlines() if line.strip()]

rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def part1():
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                neighbor_rolls = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        neighbor_rolls += 1
                if neighbor_rolls < 4:
                    count += 1
    print(count)  # Number of accessible rolls
    return count

def part2():
    # Make grid mutable
    grid_mutable = [list(row) for row in grid]

    total_removed = 0
    while True:
        accessible = []
        for r in range(rows):
            for c in range(cols):
                if grid_mutable[r][c] == '@':
                    neighbor_rolls = 0
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid_mutable[nr][nc] == '@':
                            neighbor_rolls += 1
                    if neighbor_rolls < 4:
                        accessible.append((r, c))

        if not accessible:
            break

        for r, c in accessible:
            grid_mutable[r][c] = '.'

        total_removed += len(accessible)

    print(total_removed)  # Total removed rolls
    return total_removed

part1()
part2()

import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def step(grid, corners_on=False):
    rows, cols = len(grid), len(grid[0])
    new_grid = [[False] * cols for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                        neighbors += 1
            
            if grid[r][c]:
                new_grid[r][c] = neighbors in (2, 3)
            else:
                new_grid[r][c] = neighbors == 3
    
    if corners_on:
        new_grid[0][0] = True
        new_grid[0][cols-1] = True
        new_grid[rows-1][0] = True
        new_grid[rows-1][cols-1] = True
    
    return new_grid

def parse_grid(lines):
    return [[c == '#' for c in line] for line in lines]

def count_on(grid):
    return sum(sum(row) for row in grid)

def part1(lines):
    grid = parse_grid(lines)
    for _ in range(100):
        grid = step(grid)
    return count_on(grid)

def part2(lines):
    grid = parse_grid(lines)
    rows, cols = len(grid), len(grid[0])
    grid[0][0] = True
    grid[0][cols-1] = True
    grid[rows-1][0] = True
    grid[rows-1][cols-1] = True
    
    for _ in range(100):
        grid = step(grid, corners_on=True)
    return count_on(grid)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

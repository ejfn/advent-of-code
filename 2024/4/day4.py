import os
import sys

def parse_input(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def part1():
    grid = parse_input(os.path.join(sys.path[0], 'input.txt'))
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # All 8 directions: right, left, down, up, and 4 diagonals
    directions = [
        (0, 1),   # right
        (0, -1),  # left
        (1, 0),   # down
        (-1, 0),  # up
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]

    target = "XMAS"
    count = 0

    def search_from(r, c, dr, dc):
        """Search for XMAS starting at (r,c) in direction (dr,dc)"""
        for i in range(len(target)):
            nr, nc = r + i * dr, c + i * dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                return False
            if grid[nr][nc] != target[i]:
                return False
        return True

    # Try starting from every position
    for r in range(rows):
        for c in range(cols):
            # Try all 8 directions
            for dr, dc in directions:
                if search_from(r, c, dr, dc):
                    count += 1

    return count

def part2():
    grid = parse_input(os.path.join(sys.path[0], 'input.txt'))
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    count = 0

    # For each position, check if it's the center of an X-MAS
    # The center must be 'A', and the diagonals must spell MAS or SAM
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != 'A':
                continue

            # Check the two diagonals
            # Diagonal 1: top-left to bottom-right
            diag1 = grid[r-1][c-1] + grid[r][c] + grid[r+1][c+1]
            # Diagonal 2: top-right to bottom-left
            diag2 = grid[r-1][c+1] + grid[r][c] + grid[r+1][c-1]

            # Both diagonals must be either "MAS" or "SAM"
            if (diag1 == "MAS" or diag1 == "SAM") and (diag2 == "MAS" or diag2 == "SAM"):
                count += 1

    return count

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

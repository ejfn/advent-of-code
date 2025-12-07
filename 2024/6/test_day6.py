import os
import sys

def parse_input(filename):
    """Parse the map and find the guard's starting position"""
    with open(os.path.join(sys.path[0], filename), 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]

    # Find the guard's starting position and direction
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    guard_pos = None
    guard_dir = None

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] in directions:
                guard_pos = (r, c)
                guard_dir = directions[grid[r][c]]
                grid[r][c] = '.'  # Clear the starting position
                break
        if guard_pos:
            break

    return grid, guard_pos, guard_dir

def turn_right(direction):
    """Turn 90 degrees to the right"""
    dr, dc = direction
    return (dc, -dr)

def part1(filename):
    grid, guard_pos, guard_dir = parse_input(filename)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    visited = set()
    visited.add(guard_pos)

    r, c = guard_pos
    dr, dc = guard_dir

    while True:
        # Calculate next position
        next_r = r + dr
        next_c = c + dc

        # Check if guard leaves the map
        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            break

        # Check if there's an obstacle
        if grid[next_r][next_c] == '#':
            # Turn right
            dr, dc = turn_right((dr, dc))
        else:
            # Move forward
            r, c = next_r, next_c
            visited.add((r, c))

    return len(visited)

if __name__ == "__main__":
    result = part1('test_input.txt')
    print(f"Part 1 test result: {result} (expected 41)")

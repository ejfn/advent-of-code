import os
import sys

def parse_input():
    """Parse the map and find the guard's starting position"""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
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
    # (dr, dc) -> turn right
    # up (-1, 0) -> right (0, 1)
    # right (0, 1) -> down (1, 0)
    # down (1, 0) -> left (0, -1)
    # left (0, -1) -> up (-1, 0)
    dr, dc = direction
    return (dc, -dr)

def part1():
    grid, guard_pos, guard_dir = parse_input()
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

def part2():
    """Find positions where placing an obstruction causes a loop"""
    grid, start_pos, start_dir = parse_input()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    def causes_loop(grid, obstruction_pos):
        """Check if placing an obstruction at given position causes a loop"""
        if grid[obstruction_pos[0]][obstruction_pos[1]] == '#':
            return False
        if obstruction_pos == start_pos:
            return False

        # Temporarily place obstruction
        original = grid[obstruction_pos[0]][obstruction_pos[1]]
        grid[obstruction_pos[0]][obstruction_pos[1]] = '#'

        # Simulate guard movement
        visited_states = set()
        r, c = start_pos
        dr, dc = start_dir

        while True:
            state = (r, c, dr, dc)
            if state in visited_states:
                # Loop detected
                grid[obstruction_pos[0]][obstruction_pos[1]] = original
                return True
            visited_states.add(state)

            # Calculate next position
            next_r = r + dr
            next_c = c + dc

            # Check if guard leaves the map
            if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
                grid[obstruction_pos[0]][obstruction_pos[1]] = original
                return False

            # Check if there's an obstacle
            if grid[next_r][next_c] == '#':
                # Turn right
                dr, dc = turn_right((dr, dc))
            else:
                # Move forward
                r, c = next_r, next_c

    # First, get all positions the guard visits in original path
    # Only those positions are candidates for obstruction placement
    r, c = start_pos
    dr, dc = start_dir
    path_positions = set()

    while True:
        next_r = r + dr
        next_c = c + dc

        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            break

        if grid[next_r][next_c] == '#':
            dr, dc = turn_right((dr, dc))
        else:
            r, c = next_r, next_c
            path_positions.add((r, c))

    # Test each position on the path
    loop_count = 0
    for pos in path_positions:
        if causes_loop(grid, pos):
            loop_count += 1

    return loop_count

if __name__ == "__main__":
    print(part1())
    print(part2())

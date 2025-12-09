import os
import sys
import re

def parse_input(lines):
    """Parse the input into a map and a list of instructions."""
    # Find the blank line that separates map from path
    blank_idx = next(i for i, line in enumerate(lines) if line.strip() == '')

    # Parse the map
    map_lines = lines[:blank_idx]
    # Pad all lines to the same length
    max_len = max(len(line) for line in map_lines)
    grid = [line.ljust(max_len) for line in map_lines]

    # Parse the path
    path_line = lines[blank_idx + 1].strip()
    instructions = []
    pattern = r'(\d+|[LR])'
    for match in re.finditer(pattern, path_line):
        token = match.group(1)
        if token in 'LR':
            instructions.append(token)
        else:
            instructions.append(int(token))

    return grid, instructions

def find_start(grid):
    """Find the starting position (leftmost open tile in top row)."""
    top_row = grid[0]
    for col, ch in enumerate(top_row):
        if ch == '.':
            return 0, col
    return None

def wrap_around(grid, row, col, facing):
    """Find the wrapped position by going in the opposite direction."""
    # Directions: 0=right, 1=down, 2=left, 3=up
    dr, dc = [(0, 1), (1, 0), (0, -1), (-1, 0)][facing]

    # Go backwards until we hit space or out of bounds
    reverse_dr, reverse_dc = -dr, -dc
    new_row, new_col = row, col

    # Keep going backwards while we're on valid tiles
    while True:
        test_row = new_row + reverse_dr
        test_col = new_col + reverse_dc

        # Check if out of bounds or space
        if (test_row < 0 or test_row >= len(grid) or
            test_col < 0 or test_col >= len(grid[test_row]) or
            grid[test_row][test_col] == ' '):
            break

        new_row, new_col = test_row, test_col

    return new_row, new_col

def move(grid, row, col, facing, steps):
    """Move the specified number of steps in the current direction."""
    dr, dc = [(0, 1), (1, 0), (0, -1), (-1, 0)][facing]

    for _ in range(steps):
        next_row = row + dr
        next_col = col + dc

        # Check if we need to wrap
        if (next_row < 0 or next_row >= len(grid) or
            next_col < 0 or next_col >= len(grid[next_row]) or
            grid[next_row][next_col] == ' '):
            # Wrap around
            next_row, next_col = wrap_around(grid, row, col, facing)

        # Check if we hit a wall
        if grid[next_row][next_col] == '#':
            break

        # Move to the next position
        row, col = next_row, next_col

    return row, col

def turn(facing, direction):
    """Turn left or right."""
    if direction == 'R':
        return (facing + 1) % 4
    else:  # 'L'
        return (facing - 1) % 4

def simulate(grid, instructions):
    """Simulate the path and return final position and facing."""
    row, col = find_start(grid)
    facing = 0  # 0=right, 1=down, 2=left, 3=up

    for instruction in instructions:
        if isinstance(instruction, int):
            row, col = move(grid, row, col, facing, instruction)
        else:
            facing = turn(facing, instruction)

    return row, col, facing

def calculate_password(row, col, facing):
    """Calculate the password from final position and facing."""
    return 1000 * (row + 1) + 4 * (col + 1) + facing

def run_example():
    """Test with the example from the problem."""
    example_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

    lines = example_input.split('\n')
    grid, instructions = parse_input(lines)
    row, col, facing = simulate(grid, instructions)
    password = calculate_password(row, col, facing)

    print(f"Example: row={row+1}, col={col+1}, facing={facing}, password={password}")
    print(f"Expected: row=6, col=8, facing=0, password=6032")
    assert password == 6032, f"Expected 6032, got {password}"

def part1():
    """Solve part 1."""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        lines = f.read().split('\n')

    grid, instructions = parse_input(lines)
    row, col, facing = simulate(grid, instructions)
    password = calculate_password(row, col, facing)

    return password

def part2():
    """Solve part 2."""
    # Part 2 will require cube wrapping logic
    return 0

if __name__ == "__main__":
    run_example()
    print()
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

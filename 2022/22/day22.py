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

def detect_cube_size(grid):
    """Detect the size of each cube face."""
    # Count non-space tiles
    total_tiles = sum(1 for row in grid for ch in row if ch in '.#')
    # Each cube has 6 faces, so total_tiles = 6 * face_size^2
    face_size = int((total_tiles / 6) ** 0.5)
    return face_size

def identify_faces(grid, face_size):
    """Identify which faces are present in the grid."""
    faces = {}
    face_id = 0

    for r in range(0, len(grid), face_size):
        for c in range(0, len(grid[0]), face_size):
            # Check if this is a valid face (has non-space content)
            if r < len(grid) and c < len(grid[r]) and grid[r][c] != ' ':
                faces[face_id] = (r, c)
                face_id += 1

    return faces

def get_cube_transitions_example():
    """
    Define cube transitions for the example (4x4 faces).

    Layout:
        1
      234
        56

    Returns a dict: (face_id, edge_dir) -> (new_face_id, new_dir)
    edge_dir: 0=right, 1=down, 2=left, 3=up
    """
    # This is the example cube net. Need to manually define connections.
    # Face layout in grid coordinates (each face is 4x4):
    # Face 1: (0, 8)
    # Face 2: (4, 0)
    # Face 3: (4, 4)
    # Face 4: (4, 8)
    # Face 5: (8, 8)
    # Face 6: (8, 12)

    transitions = {}
    # Face 1 (top)
    transitions[(0, 0)] = (5, 2)  # right -> face 6 left (reversed)
    transitions[(0, 1)] = (3, 1)  # down -> face 4 down
    transitions[(0, 2)] = (2, 1)  # left -> face 3 down (rotated)
    transitions[(0, 3)] = (1, 1)  # up -> face 2 down (reversed)

    # Face 2 (left)
    transitions[(1, 0)] = (2, 0)  # right -> face 3 right
    transitions[(1, 1)] = (4, 3)  # down -> face 5 up (reversed)
    transitions[(1, 2)] = (5, 3)  # left -> face 6 up (rotated)
    transitions[(1, 3)] = (0, 1)  # up -> face 1 down (reversed)

    # Face 3 (middle)
    transitions[(2, 0)] = (3, 0)  # right -> face 4 right
    transitions[(2, 1)] = (4, 0)  # down -> face 5 right (rotated)
    transitions[(2, 2)] = (1, 2)  # left -> face 2 left
    transitions[(2, 3)] = (0, 0)  # up -> face 1 right (rotated)

    # Face 4 (right in middle row)
    transitions[(3, 0)] = (5, 1)  # right -> face 6 down (rotated)
    transitions[(3, 1)] = (4, 1)  # down -> face 5 down
    transitions[(3, 2)] = (2, 2)  # left -> face 3 left
    transitions[(3, 3)] = (0, 3)  # up -> face 1 up

    # Face 5 (bottom left)
    transitions[(4, 0)] = (5, 0)  # right -> face 6 right
    transitions[(4, 1)] = (1, 3)  # down -> face 2 up (reversed)
    transitions[(4, 2)] = (2, 3)  # left -> face 3 up (rotated)
    transitions[(4, 3)] = (3, 3)  # up -> face 4 up

    # Face 6 (bottom right)
    transitions[(5, 0)] = (0, 2)  # right -> face 1 left (reversed)
    transitions[(5, 1)] = (1, 0)  # down -> face 2 right (rotated)
    transitions[(5, 2)] = (4, 2)  # left -> face 5 left
    transitions[(5, 3)] = (3, 2)  # up -> face 4 left (rotated)

    return transitions

def wrap_cube_real(row, col, facing):
    """
    Hard-coded cube wrapping for the real input (50x50 faces).

    Layout (face numbers):
       01
       2
      34
      5

    Grid coordinates:
    Face 0: rows 0-49, cols 50-99
    Face 1: rows 0-49, cols 100-149
    Face 2: rows 50-99, cols 50-99
    Face 3: rows 100-149, cols 0-49
    Face 4: rows 100-149, cols 50-99
    Face 5: rows 150-199, cols 0-49
    """
    # Determine current face and local position
    if 0 <= row < 50:
        if 50 <= col < 100:
            face = 0
            lr, lc = row, col - 50
        else:  # 100 <= col < 150
            face = 1
            lr, lc = row, col - 100
    elif 50 <= row < 100:
        face = 2
        lr, lc = row - 50, col - 50
    elif 100 <= row < 150:
        if 0 <= col < 50:
            face = 3
            lr, lc = row - 100, col
        else:  # 50 <= col < 100
            face = 4
            lr, lc = row - 100, col - 50
    else:  # 150 <= row < 200
        face = 5
        lr, lc = row - 150, col

    # Handle wrapping based on face and direction
    if face == 0:
        if facing == 0:  # right -> face 1
            return row, col + 1, facing
        elif facing == 1:  # down -> face 2
            return row + 1, col, facing
        elif facing == 2:  # left -> face 3, reversed
            return 149 - lr, 0, 0  # enter face 3 from left, facing right
        else:  # up -> face 5, rotated
            return 150 + lc, 0, 0  # enter face 5 from left, facing right
    elif face == 1:
        if facing == 0:  # right -> face 4, reversed
            return 149 - lr, 99, 2  # enter face 4 from right, facing left
        elif facing == 1:  # down -> face 2, rotated
            return 50 + lc, 99, 2  # enter face 2 from right, facing left
        elif facing == 2:  # left -> face 0
            return row, col - 1, facing
        else:  # up -> face 5, straight
            return 199, lc, 3  # enter face 5 from bottom, facing up
    elif face == 2:
        if facing == 0:  # right -> face 1, rotated
            return 49, 100 + lr, 3  # enter face 1 from bottom, facing up
        elif facing == 1:  # down -> face 4
            return row + 1, col, facing
        elif facing == 2:  # left -> face 3, rotated
            return 100, lr, 1  # enter face 3 from top, facing down
        else:  # up -> face 0
            return row - 1, col, facing
    elif face == 3:
        if facing == 0:  # right -> face 4
            return row, col + 1, facing
        elif facing == 1:  # down -> face 5
            return row + 1, col, facing
        elif facing == 2:  # left -> face 0, reversed
            return 49 - lr, 50, 0  # enter face 0 from left, facing right
        else:  # up -> face 2, rotated
            return 50 + lc, 50, 0  # enter face 2 from left, facing right
    elif face == 4:
        if facing == 0:  # right -> face 1, reversed
            return 49 - lr, 149, 2  # enter face 1 from right, facing left
        elif facing == 1:  # down -> face 5, rotated
            return 150 + lc, 49, 2  # enter face 5 from right, facing left
        elif facing == 2:  # left -> face 3
            return row, col - 1, facing
        else:  # up -> face 2
            return row - 1, col, facing
    else:  # face == 5
        if facing == 0:  # right -> face 4, rotated
            return 149, 50 + lr, 3  # enter face 4 from bottom, facing up
        elif facing == 1:  # down -> face 1, straight
            return 0, 100 + lc, 1  # enter face 1 from top, facing down
        elif facing == 2:  # left -> face 0, rotated
            return 0, 50 + lr, 1  # enter face 0 from top, facing down
        else:  # up -> face 3
            return row - 1, col, facing

    return None, None, facing

def move_cube_real(grid, row, col, facing, steps):
    """Move with cube wrapping for real input."""
    dr, dc = [(0, 1), (1, 0), (0, -1), (-1, 0)][facing]

    for _ in range(steps):
        next_row = row + dr
        next_col = col + dc
        next_facing = facing

        # Check if we need to wrap
        if (next_row < 0 or next_row >= len(grid) or
            next_col < 0 or next_col >= len(grid[next_row]) or
            grid[next_row][next_col] == ' '):
            # Wrap around the cube
            next_row, next_col, next_facing = wrap_cube_real(row, col, facing)

            if next_row is None:
                break

        # Check if we hit a wall
        if grid[next_row][next_col] == '#':
            break

        # Move to the next position
        row, col, facing = next_row, next_col, next_facing
        dr, dc = [(0, 1), (1, 0), (0, -1), (-1, 0)][facing]

    return row, col, facing

def simulate_cube_real(grid, instructions):
    """Simulate with cube wrapping for real input."""
    row, col = find_start(grid)
    facing = 0

    for instruction in instructions:
        if isinstance(instruction, int):
            row, col, facing = move_cube_real(grid, row, col, facing, instruction)
        else:
            facing = turn(facing, instruction)

    return row, col, facing

def part2():
    """Solve part 2."""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        lines = f.read().split('\n')

    grid, instructions = parse_input(lines)
    row, col, facing = simulate_cube_real(grid, instructions)
    password = calculate_password(row, col, facing)

    return password

if __name__ == "__main__":
    run_example()
    print()
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

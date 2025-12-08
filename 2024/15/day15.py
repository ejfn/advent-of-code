import os
import sys

def parse_input(filename):
    with open(filename) as f:
        content = f.read()

    # Split by empty line
    parts = content.split('\n\n')
    grid_lines = parts[0].strip().split('\n')
    moves = parts[1].replace('\n', '').strip()

    # Parse grid
    grid = [list(line) for line in grid_lines]

    # Find robot position
    robot_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '@':
                robot_pos = (r, c)
                grid[r][c] = '.'  # Replace robot with empty space
                break
        if robot_pos:
            break

    return grid, robot_pos, moves

def print_grid(grid, robot_pos):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) == robot_pos:
                print('@', end='')
            else:
                print(grid[r][c], end='')
        print()
    print()

def try_move(grid, robot_pos, direction):
    """Try to move robot in given direction. Returns new robot position."""
    dr, dc = direction
    new_r, new_c = robot_pos[0] + dr, robot_pos[1] + dc

    # Check what's at the new position
    if grid[new_r][new_c] == '#':
        # Hit a wall, can't move
        return robot_pos
    elif grid[new_r][new_c] == '.':
        # Empty space, just move
        return (new_r, new_c)
    elif grid[new_r][new_c] == 'O':
        # There's a box, try to push it
        # Find all consecutive boxes in this direction
        check_r, check_c = new_r, new_c
        boxes = []
        while grid[check_r][check_c] == 'O':
            boxes.append((check_r, check_c))
            check_r += dr
            check_c += dc

        # Check what's after the boxes
        if grid[check_r][check_c] == '#':
            # Can't push boxes into a wall
            return robot_pos
        elif grid[check_r][check_c] == '.':
            # Can push boxes
            # Move the furthest box first
            grid[check_r][check_c] = 'O'
            grid[new_r][new_c] = '.'
            return (new_r, new_c)

    return robot_pos

def simulate(grid, robot_pos, moves):
    """Simulate all moves and return final robot position."""
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    for move in moves:
        direction = directions[move]
        robot_pos = try_move(grid, robot_pos, direction)

    return robot_pos

def calculate_gps_sum(grid):
    """Calculate sum of GPS coordinates for all boxes."""
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                gps = 100 * r + c
                total += gps
    return total

def run_example():
    """Test with the small example from the puzzle."""
    example = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

    with open('/tmp/example.txt', 'w') as f:
        f.write(example)

    grid, robot_pos, moves = parse_input('/tmp/example.txt')

    print("Initial state:")
    print_grid(grid, robot_pos)
    print(f"Robot at: {robot_pos}")
    print(f"Moves: {moves}")
    print()

    final_pos = simulate(grid, robot_pos, moves)

    print("Final state:")
    print_grid(grid, final_pos)

    gps_sum = calculate_gps_sum(grid)
    print(f"GPS sum: {gps_sum}")
    print(f"Expected: 2028")

def part1():
    input_file = os.path.join(sys.path[0], 'input.txt')
    grid, robot_pos, moves = parse_input(input_file)

    # Simulate all moves
    final_pos = simulate(grid, robot_pos, moves)

    # Calculate GPS sum
    result = calculate_gps_sum(grid)
    return result

def part2():
    input_file = os.path.join(sys.path[0], 'input.txt')
    # Part 2 to be implemented
    return 0

if __name__ == '__main__':
    print("Testing with example:")
    run_example()
    print("\n" + "="*50 + "\n")

    print("Part 1:", part1())
    print("Part 2:", part2())

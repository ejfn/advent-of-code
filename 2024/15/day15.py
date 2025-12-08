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

def scale_up_grid(grid):
    """Scale up the grid according to Part 2 rules."""
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == '#':
                new_row.extend(['#', '#'])
            elif cell == 'O':
                new_row.extend(['[', ']'])
            elif cell == '.':
                new_row.extend(['.', '.'])
            elif cell == '@':
                new_row.extend(['@', '.'])
        new_grid.append(new_row)
    return new_grid

def can_push_boxes_vertical(grid, boxes_to_check, dr):
    """Check if boxes can be pushed vertically. Returns (can_push, all_boxes_to_move)."""
    all_boxes = set()
    to_check = list(boxes_to_check)

    while to_check:
        r, c = to_check.pop(0)
        if (r, c) in all_boxes:
            continue

        # Get the full box (both [ and ])
        if grid[r][c] == '[':
            all_boxes.add((r, c))
            all_boxes.add((r, c+1))
            # Check what's ahead of both parts
            new_r = r + dr
            left_ahead = grid[new_r][c]
            right_ahead = grid[new_r][c+1]

            if left_ahead == '#' or right_ahead == '#':
                return False, []
            if left_ahead in ['[', ']']:
                to_check.append((new_r, c))
            if right_ahead in ['[', ']']:
                to_check.append((new_r, c+1))

        elif grid[r][c] == ']':
            all_boxes.add((r, c))
            all_boxes.add((r, c-1))
            # Check what's ahead of both parts
            new_r = r + dr
            left_ahead = grid[new_r][c-1]
            right_ahead = grid[new_r][c]

            if left_ahead == '#' or right_ahead == '#':
                return False, []
            if left_ahead in ['[', ']']:
                to_check.append((new_r, c-1))
            if right_ahead in ['[', ']']:
                to_check.append((new_r, c))

    return True, all_boxes

def try_move_wide(grid, robot_pos, direction):
    """Try to move robot in wide grid. Returns new robot position."""
    dr, dc = direction
    new_r, new_c = robot_pos[0] + dr, robot_pos[1] + dc

    # Check what's at the new position
    if grid[new_r][new_c] == '#':
        return robot_pos
    elif grid[new_r][new_c] == '.':
        return (new_r, new_c)
    elif grid[new_r][new_c] in ['[', ']']:
        # Horizontal movement (simpler)
        if dc != 0:
            # Find all consecutive box parts
            check_c = new_c
            while grid[new_r][check_c] in ['[', ']']:
                check_c += dc

            # Check what's after
            if grid[new_r][check_c] == '#':
                return robot_pos
            elif grid[new_r][check_c] == '.':
                # Shift everything
                if dc > 0:  # Moving right
                    for c in range(check_c, new_c, -1):
                        grid[new_r][c] = grid[new_r][c-1]
                else:  # Moving left
                    for c in range(check_c, new_c):
                        grid[new_r][c] = grid[new_r][c+1]
                grid[new_r][new_c] = '.'
                return (new_r, new_c)
        else:
            # Vertical movement (complex - can push multiple boxes)
            can_push, boxes_to_move = can_push_boxes_vertical(grid, [(new_r, new_c)], dr)

            if not can_push:
                return robot_pos

            # Sort boxes by row (move furthest first to avoid overwriting)
            if dr > 0:  # Moving down
                sorted_boxes = sorted(boxes_to_move, key=lambda x: -x[0])
            else:  # Moving up
                sorted_boxes = sorted(boxes_to_move, key=lambda x: x[0])

            # Move all boxes
            for r, c in sorted_boxes:
                grid[r + dr][c] = grid[r][c]
                grid[r][c] = '.'

            return (new_r, new_c)

    return robot_pos

def simulate_wide(grid, robot_pos, moves):
    """Simulate all moves in wide grid."""
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    for move in moves:
        direction = directions[move]
        robot_pos = try_move_wide(grid, robot_pos, direction)

    return robot_pos

def calculate_gps_sum_wide(grid):
    """Calculate sum of GPS coordinates for wide boxes (use left edge '[')."""
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '[':
                gps = 100 * r + c
                total += gps
    return total

def run_example_part2():
    """Test Part 2 with examples."""
    # Small example
    example = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

    with open('/tmp/example2.txt', 'w') as f:
        f.write(example)

    grid, robot_pos, moves = parse_input('/tmp/example2.txt')
    grid = scale_up_grid(grid)
    robot_pos = (robot_pos[0], robot_pos[1] * 2)

    print("Initial state (scaled):")
    print_grid(grid, robot_pos)

    final_pos = simulate_wide(grid, robot_pos, moves)

    print("Final state:")
    print_grid(grid, final_pos)

    # Large example
    large_example = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    with open('/tmp/example3.txt', 'w') as f:
        f.write(large_example)

    grid, robot_pos, moves = parse_input('/tmp/example3.txt')
    grid = scale_up_grid(grid)
    robot_pos = (robot_pos[0], robot_pos[1] * 2)

    final_pos = simulate_wide(grid, robot_pos, moves)

    print("Large example final state:")
    print_grid(grid, final_pos)

    gps_sum = calculate_gps_sum_wide(grid)
    print(f"GPS sum: {gps_sum}")
    print(f"Expected: 9021")

def part2():
    input_file = os.path.join(sys.path[0], 'input.txt')
    grid, robot_pos, moves = parse_input(input_file)

    # Scale up the grid
    grid = scale_up_grid(grid)
    robot_pos = (robot_pos[0], robot_pos[1] * 2)

    # Simulate
    final_pos = simulate_wide(grid, robot_pos, moves)

    # Calculate GPS sum
    result = calculate_gps_sum_wide(grid)
    return result

if __name__ == '__main__':
    print("Testing Part 1 with example:")
    run_example()
    print("\n" + "="*50 + "\n")

    print("Testing Part 2 with examples:")
    run_example_part2()
    print("\n" + "="*50 + "\n")

    print("Part 1:", part1())
    print("Part 2:", part2())

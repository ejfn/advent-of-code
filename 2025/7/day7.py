import os
import sys
from collections import deque

def part1():
    # Read the input
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    # Find the starting position 'S'
    start_row = -1
    start_col = -1
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == 'S':
                start_row = r
                start_col = c
                break
        if start_row != -1:
            break

    # Simulate the beam splitting
    # Beams always move downward
    # When a beam hits a splitter, it creates two new beams at positions left and right of the splitter
    # Those new beams continue moving downward from their new positions

    split_count = 0

    # Track active beam positions (just column positions, since all beams move downward)
    # Start with the beam at column start_col
    active_columns = {start_col}

    # Process row by row, moving downward
    for row in range(start_row + 1, len(grid)):
        new_columns = set()

        for col in active_columns:
            # Check what's at this position
            if col < 0 or col >= len(grid[row]):
                continue

            cell = grid[row][col]

            if cell == '.':
                # Beam continues downward
                new_columns.add(col)
            elif cell == '^':
                # Splitter - beam is split
                split_count += 1
                # Create two new beams at left and right positions
                if col - 1 >= 0:
                    new_columns.add(col - 1)
                if col + 1 < len(grid[row]):
                    new_columns.add(col + 1)
            else:
                # Empty or other - beam continues
                new_columns.add(col)

        active_columns = new_columns

        # If no beams left, stop
        if not active_columns:
            break

    return split_count

def part2():
    # Part 2 will be implemented after part 1 is solved
    pass

if __name__ == "__main__":
    print("Part 1:", part1())
    # print("Part 2:", part2())

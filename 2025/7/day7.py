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

    # Track the number of timelines at each column position
    # Start with 1 timeline at the starting column
    timeline_counts = {start_col: 1}

    # Process row by row, moving downward
    for row in range(start_row + 1, len(grid)):
        new_timeline_counts = {}

        for col, count in timeline_counts.items():
            # Check what's at this position
            if col < 0 or col >= len(grid[row]):
                continue

            cell = grid[row][col]

            if cell == '.':
                # Particle continues downward in the same timeline(s)
                new_timeline_counts[col] = new_timeline_counts.get(col, 0) + count
            elif cell == '^':
                # Splitter - each timeline splits into 2 timelines
                # One goes left, one goes right
                left_col = col - 1
                right_col = col + 1

                if left_col >= 0:
                    new_timeline_counts[left_col] = new_timeline_counts.get(left_col, 0) + count
                if right_col < len(grid[row]):
                    new_timeline_counts[right_col] = new_timeline_counts.get(right_col, 0) + count
            else:
                # Empty or other - particle continues
                new_timeline_counts[col] = new_timeline_counts.get(col, 0) + count

        timeline_counts = new_timeline_counts

        # If no timelines left, stop
        if not timeline_counts:
            break

    # Return the total number of timelines
    return sum(timeline_counts.values())

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

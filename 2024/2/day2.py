import os
import sys


def is_safe(levels):
    """Check if a report is safe according to the rules."""
    if len(levels) < 2:
        return True

    # Check if all increasing or all decreasing
    differences = [levels[i+1] - levels[i] for i in range(len(levels) - 1)]

    # All differences must be in the same direction (all positive or all negative)
    # and have absolute value between 1 and 3
    all_increasing = all(1 <= d <= 3 for d in differences)
    all_decreasing = all(-3 <= d <= -1 for d in differences)

    return all_increasing or all_decreasing


def part1():
    """Solve part 1."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        lines = f.read().strip().split('\n')

    safe_count = 0
    for line in lines:
        levels = list(map(int, line.split()))
        if is_safe(levels):
            safe_count += 1

    return safe_count


def part2():
    """Solve part 2."""
    # To be implemented after Part 1 is solved
    pass


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    # print(f"Part 2: {part2()}")

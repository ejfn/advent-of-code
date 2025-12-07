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


def is_safe_with_dampener(levels):
    """Check if a report is safe with the Problem Dampener (can remove one level)."""
    # First check if it's already safe
    if is_safe(levels):
        return True

    # Try removing each level one at a time
    for i in range(len(levels)):
        # Create a new list without the level at index i
        modified_levels = levels[:i] + levels[i+1:]
        if is_safe(modified_levels):
            return True

    return False


def part2():
    """Solve part 2."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        lines = f.read().strip().split('\n')

    safe_count = 0
    for line in lines:
        levels = list(map(int, line.split()))
        if is_safe_with_dampener(levels):
            safe_count += 1

    return safe_count


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

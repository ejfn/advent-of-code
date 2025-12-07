import os
import sys

def parse_input(filename):
    """Parse input file into two lists of location IDs."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    left_list = []
    right_list = []

    for line in lines:
        line = line.strip()
        if line:
            parts = line.split()
            left_list.append(int(parts[0]))
            right_list.append(int(parts[1]))

    return left_list, right_list

def part1():
    """Calculate total distance between sorted lists."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    left_list, right_list = parse_input(input_file)

    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate sum of absolute differences
    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))

    return total_distance

def part2():
    """Part 2 solution - to be implemented when unlocked."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    left_list, right_list = parse_input(input_file)

    # Calculate similarity score
    # For each number in left list, count occurrences in right list
    # Multiply the number by its count and sum all results
    from collections import Counter
    right_counts = Counter(right_list)

    similarity_score = sum(num * right_counts[num] for num in left_list)

    return similarity_score

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

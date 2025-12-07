import os
import sys
import re


def part1():
    # Load input
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        data = f.read()

    # Find all valid mul(X,Y) instructions
    # Pattern: mul followed by ( then 1-3 digits, comma, 1-3 digits, then )
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, data)

    # Calculate sum of all multiplications
    total = 0
    for x, y in matches:
        total += int(x) * int(y)

    return total


def part2():
    # Load input
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        data = f.read()

    # TODO: Implement part 2
    return 0


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

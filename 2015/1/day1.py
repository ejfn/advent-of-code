import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def part1(data):
    return data.count('(') - data.count(')')

def part2(data):
    floor = 0
    for i, c in enumerate(data, 1):
        floor += 1 if c == '(' else -1
        if floor == -1:
            return i
    return None

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

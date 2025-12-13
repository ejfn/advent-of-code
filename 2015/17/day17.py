import os
import sys
from itertools import combinations

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [int(line.strip()) for line in f if line.strip()]

def part1(containers):
    target = 150
    count = 0
    for r in range(1, len(containers) + 1):
        for combo in combinations(containers, r):
            if sum(combo) == target:
                count += 1
    return count

def part2(containers):
    target = 150
    for r in range(1, len(containers) + 1):
        count = sum(1 for combo in combinations(containers, r) if sum(combo) == target)
        if count > 0:
            return count
    return 0

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

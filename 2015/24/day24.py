import os
import sys
from itertools import combinations
from functools import reduce
from operator import mul

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [int(line.strip()) for line in f if line.strip()]

def find_min_qe(packages, num_groups):
    target = sum(packages) // num_groups
    
    for size in range(1, len(packages)):
        qes = []
        for combo in combinations(packages, size):
            if sum(combo) == target:
                qe = reduce(mul, combo)
                qes.append(qe)
        if qes:
            return min(qes)
    return None

def part1(packages):
    return find_min_qe(packages, 3)

def part2(packages):
    return find_min_qe(packages, 4)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

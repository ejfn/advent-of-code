import os
import sys
from itertools import groupby

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def look_and_say(s):
    result = []
    for digit, group in groupby(s):
        count = len(list(group))
        result.append(str(count))
        result.append(digit)
    return ''.join(result)

def apply_n_times(s, n):
    for _ in range(n):
        s = look_and_say(s)
    return s

def part1(s):
    return len(apply_n_times(s, 40))

def part2(s):
    return len(apply_n_times(s, 50))

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(s) for s in f.readline().split(',')]

start = min(numbers)
end = max(numbers)


def part1():
    fuel = defaultdict(lambda: 0)
    for n in range(start, end + 1):
        for i in numbers:
            fuel[n] += abs(n - i)
    return min(fuel.values())


def part2():
    fuel = defaultdict(lambda: 0)
    for n in range(start, end + 1):
        for i in numbers:
            d = abs(n-i)
            fuel[n] += d * (1 + d) / 2
    return int(min(fuel.values()))


print(part1())  # 345035
print(part2())  # 97038163

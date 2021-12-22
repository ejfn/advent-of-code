from collections import defaultdict
import itertools
import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(s) for s in f.readline().split(',')]

start = min(numbers)
end = max(numbers)


def part1():
    fuel = defaultdict(lambda: 0)
    for i, j in itertools.product(range(start, end), numbers):
        fuel[i] += abs(i - j)
    print(min(fuel.values()))


def part2():
    fuel = defaultdict(lambda: 0)
    for i, j in itertools.product(range(start, end), numbers):
        d = abs(i-j)
        fuel[i] += d * (1 + d) / 2
    print(int(min(fuel.values())))


part1()  # 345035
part2()  # 97038163

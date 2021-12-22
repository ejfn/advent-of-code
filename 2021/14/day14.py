from collections import defaultdict
import itertools
import os
import sys

start = ''
rules = {}
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        line = line.strip()
        splits = line.split(' -> ')
        if len(splits) == 2:
            rules[splits[0]] = splits[1]
        elif line != '':
            start = line


def next_polymer(curr, count):
    next = defaultdict(lambda: 0)
    for k in filter(lambda x: x in rules, curr):
        v, m = curr[k], rules[k]
        count[m] += v
        next[k[0] + m] += v
        next[m + k[1]] += v
    return next


def after_steps(steps):
    count = defaultdict(lambda: 0)
    next = defaultdict(lambda: 0)
    count[start[-1]] = 1
    for i, j in itertools.pairwise(start):
        count[i] += 1
        next[i + j] += 1
    for _ in range(steps):
        next = next_polymer(next, count)
    return max(count.values()) - min(count.values())


def part1(): print(after_steps(10))
def part2(): print(after_steps(40))


part1()  # 2408
part2()  # 2651311098752

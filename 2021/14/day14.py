from collections import defaultdict
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
    for k, v in curr.items():
        if k in rules:
            m = rules[k]
            count[m] += v
            next[k[0] + m] += v
            next[m + k[1]] += v
    return next


def after_steps(steps):
    count = defaultdict(lambda: 0)
    next = defaultdict(lambda: 0)
    for i, s in enumerate(start):
        count[s] += 1
        if i < len(start) - 1:
            next[start[i:i+2]] += 1
    for _ in range(steps):
        next = next_polymer(next, count)
    return max(count.values()) - min(count.values())


def part1(): return after_steps(10)
def part2(): return after_steps(40)


print(part1())  # 2408
print(part2())  # 2651311098752

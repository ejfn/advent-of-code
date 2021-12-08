from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(i) for i in f.readline().split(',')]


def next_day(counts):
    split = counts[0]
    for i in range(0, 8):
        counts[i] = counts[i+1]
    counts[6] += split
    counts[8] = split


def after_days(days):
    counts = defaultdict(lambda: 0)
    for i in numbers:
        counts[i] += 1
    for i in range(days):
        next_day(counts)
    return sum(counts.values())


print(after_days(80))
print(after_days(256))

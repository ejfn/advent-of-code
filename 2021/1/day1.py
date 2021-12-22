import itertools
import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(i) for i in f.readlines()]


def part1():
    print(sum([1 for i, j in itertools.pairwise(numbers) if i < j]))


def part2():
    print(sum([1 for i in range(len(numbers)-3)
          if sum(numbers[i:i+3]) < sum(numbers[i+1:i+4])]))


part1()  # 1527
part2()  # 1575

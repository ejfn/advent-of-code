import os
import sys
import itertools

numbers = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(x[:-1]) for x in f]


def part1():
    for i, j in itertools.combinations(numbers, 2):
        if i + j == 2020:
            print(i * j)
            return


def part2():
    for i, j, k in itertools.combinations(numbers, 3):
        if i + j + k == 2020:
            print(i * j * k)
            return


part1()  # 1014624
part2()  # 80072256

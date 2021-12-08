import os
import sys
import itertools

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = [[[int(j) for j in i.split(',')]
              for i in line.strip().split('->')] for line in f]


def iter_points(p1, p2, inc45):
    step_x = 0 if p1[0] == p2[0] else 1 if p1[0] < p2[0] else -1
    step_y = 0 if p1[1] == p2[1] else 1 if p1[1] < p2[1] else -1
    if step_x == 0:
        for i in range(p1[1], p2[1] + step_y, step_y):
            yield [p1[0], i]
    elif step_y == 0:
        for i in range(p1[0], p2[0] + step_x, step_x):
            yield [i, p1[1]]
    elif inc45:
        for i, j in zip(range(p1[0], p2[0] + step_x, step_x), range(p1[1], p2[1] + step_y, step_y)):
            yield [i, j]


def part1():
    matrix = [[0 for j in range(1000)] for i in range(1000)]
    for p1, p2 in lines:
        for i, j in iter_points(p1, p2, False):
            matrix[i][j] += 1
    return sum([1 if i >= 2 else 0 for i in itertools.chain(*matrix)])


def part2():
    matrix = [[0 for j in range(1000)] for i in range(1000)]
    for p1, p2 in lines:
        for i, j in iter_points(p1, p2, True):
            matrix[i][j] += 1
    return sum([1 if i >= 2 else 0 for i in itertools.chain(*matrix)])


print(part1())
print(part2())

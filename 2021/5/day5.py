import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = np.array([[[int(j) for j in i.split(',')]
                       for i in line.strip().split('->')] for line in f])

rows = np.max(lines[:, :,  0]) + 1
cols = np.max(lines[:, :,  1]) + 1


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
    matrix = np.zeros([rows, cols], int)
    for p1, p2 in lines:
        for i, j in iter_points(p1, p2, False):
            matrix[i, j] += 1
    return matrix[matrix >= 2].size


def part2():
    matrix = np.zeros([rows, cols], int)
    for p1, p2 in lines:
        for i, j in iter_points(p1, p2, True):
            matrix[i, j] += 1
    return matrix[matrix >= 2].size


print(part1())  # 5197
print(part2())  # 18605

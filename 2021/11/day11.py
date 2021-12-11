import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    mat = np.array([[int(i) for i in line.strip()] for line in f])

rows, cols = mat.shape


def find_adjs(i, j):
    ajds = [
        [i-1, j-1], [i-1, j], [i-1, j+1],
        [i, j-1], [i, j+1],
        [i+1, j-1], [i+1, j], [i+1, j+1]
    ]
    return filter(lambda p: p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols, ajds)


def flash(i, j, m):
    for a, b in find_adjs(i, j):
        if m[a, b] < 10:
            m[a, b] += 1
            if m[a, b] == 10:
                flash(a, b, m)


def part1():
    m = mat.copy()
    sum = 0
    for i in range(100):
        m += 1  # energy + 1
        for i, j in zip(*np.where(m == 10)):
            flash(i, j, m)
        sum += m[m == 10].size
        m[m == 10] = 0  # reset flashed
    return int(sum)


def part2():
    m = mat.copy()
    step = 0
    while True:
        m += 1  # energy + 1
        for i, j in zip(*np.where(m == 10)):
            flash(i, j, m)
        m[m == 10] = 0  # reset flashed
        step += 1
        if np.all(m == 0):
            break
    return step


print(part1())  # 1640
print(part2())  # 312

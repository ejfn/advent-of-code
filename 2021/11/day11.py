import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    arr = np.array([[int(i) for i in line.strip()] for line in f])

rows, cols = arr.shape


def find_adjs(i, j):
    ajds = [
        (i-1, j-1), (i-1, j), (i-1, j+1),
        (i, j-1), (i, j+1),
        (i+1, j-1), (i+1, j), (i+1, j+1)
    ]
    return filter(lambda p: p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols, ajds)


def flash(index, m):
    for adj in find_adjs(*index):
        if m[adj] < 10:
            m[adj] += 1
            if m[adj] == 10:
                flash(adj, m)


def part1():
    a = arr.copy()
    sum = 0
    for _ in range(100):
        a += 1  # energy + 1
        for fla in zip(*np.where(a == 10)):
            flash(fla, a)
        a[a == 10] = 0  # reset flashed
        sum += a[a == 0].size
    return sum


def part2():
    a = arr.copy()
    step = 0
    while True:
        a += 1  # energy + 1
        for fla in zip(*np.where(a == 10)):
            flash(fla, a)
        a[a == 10] = 0  # reset flashed
        step += 1
        if np.all(a == 0):
            break
    return step


print(part1())  # 1640
print(part2())  # 312

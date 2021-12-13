import os
import sys
import numpy as np

lines, folds = [], []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('fold along '):
            i, j = line[11:].split('=')
            folds.append((i, int(j)))
        elif len(line) > 0:
            lines.append(tuple(int(i) for i in line.split(',')))
arr = np.zeros([max([i[1] for i in lines]) + 1,
               max([i[0] for i in lines]) + 1], int)
for i in lines:
    arr[i[1], i[0]] = 1


def fold(arr, fold_line):
    d, n = fold_line
    axis = 0 if d == 'y' else 1
    arr = np.delete(arr, n, axis=axis)
    rows, cols = arr.shape
    gap = 2 * n - arr.shape[axis]
    zeros = np.zeros([abs(gap), cols] if axis == 0 else [rows, abs(gap)], int)
    stacks = [zeros, arr] if gap < 0 else [arr, zeros]
    arr = np.concatenate(stacks, axis=axis)
    a1, a2 = np.split(arr, 2, axis=axis)
    a2 = np.flip(a2, axis=axis)
    return a1 | a2


def part1():
    a = fold(arr, folds[0])
    return a[a == 1].size


def part2():
    a = arr
    for f in folds:
        a = fold(a, f)
    return np.array2string(a, separator='', formatter={'int': lambda x: '#' if x == 1 else ' '})


print(part1())  # 655
print(part2())  # JPZCUAUR

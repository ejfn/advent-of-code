import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    arr = np.array([[int(i) for i in line.strip()] for line in f])

rows, cols = arr.shape


def arr_to_num(arr):
    return int(''.join(arr.flatten().astype(str)), 2)


def part1():
    a = np.array([1 if sum(arr[:, col]) > rows / 2 else 0
                  for col in range(cols)])
    b = np.ones(len(a), np.int0) - a
    print(arr_to_num(a) * arr_to_num(b))


def part2():
    a, b = arr, arr
    for col in range(cols):
        if a.shape[0] > 1:
            if sum(a[:, col]) >= a.shape[0] / 2:
                a = a[a[:, col] == 1]
            else:
                a = a[a[:, col] == 0]
        if b.shape[0] > 1:
            if sum(b[:, col]) >= b.shape[0] / 2:
                b = b[b[:, col] == 0]
            else:
                b = b[b[:, col] == 1]
    print(arr_to_num(a) * arr_to_num(b))


part1()  # 3912944
part2()  # 4996233

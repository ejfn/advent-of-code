import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    input = np.array([[i for i in line.strip()] for line in f])

rows, columns = input.shape


def move_1d(arr, target='>'):
    moved = False
    cp = arr.copy()
    for i, v in enumerate(cp):
        next = i + 1 if i < len(cp) - 1 else 0
        if v == target and cp[next] == '.':
            arr[i] = '.'
            arr[next] = v
            moved = True
    return moved


def move(arr: np.array):
    moved = False
    for r in range(rows):
        moved |= move_1d(arr[r], '>')
    for c in range(columns):
        moved |= move_1d(arr[:, c], 'v')
    return moved


def part1():
    c = 1
    while move(input):
        c += 1
    print(c)


def part2():
    print("Merry Christmas!")


part1()  # 295
part2()  # Merry Christmas!

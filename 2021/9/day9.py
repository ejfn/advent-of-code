import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    arr = np.array([[int(i) for i in line.strip()] for line in f])

rows, cols = arr.shape


def find_adjs(i, j):
    pos = [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]
    return filter(lambda p: p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols, pos)


def part1():
    sum = 0
    for index, n in np.ndenumerate(arr):
        if all(n < arr[p] for p in find_adjs(*index)):
            sum += arr[index] + 1
    return sum


def find_basin(index, basin):
    last_val = arr[basin[-1]]
    adjs = find_adjs(*index)
    for a in adjs:
        if a in basin:
            continue
        val = arr[a]
        if val > last_val and val < 9:
            basin.append(a)
            find_basin(a, basin)


def part2():
    count = []
    for index, n in np.ndenumerate(arr):
        if all(n < arr[p] for p in find_adjs(*index)):
            basin = [index]
            find_basin(index, basin)
            count.append(len(basin))
            count = sorted(count, reverse=True)[:3]
    return count[0] * count[1] * count[2]


print(part1())  # 514
print(part2())  # 1103130

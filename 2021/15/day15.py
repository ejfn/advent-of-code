import os
import sys
import numpy as np
from collections import defaultdict

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    arr = np.array([[int(i) for i in line.strip()] for line in f])

rows, cols = arr.shape


def find_adjs(i, j, scale):
    pts = [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]
    return filter(lambda p: p[0] >= 0 and p[0] < rows * scale and p[1] >= 0 and p[1] < cols * scale, pts)


def dijkstra(solved: dict, unsolved: dict, scale):
    k = min(unsolved, key=unsolved.get)
    solved[k] = unsolved[k]
    del unsolved[k]
    for adj in find_adjs(k[0], k[1], scale):
        if adj in solved:
            continue
        unsolved[adj] = min(solved[k] + scaled_value(adj), unsolved[adj])


def scaled_value(x):
    i, j = x
    v = arr[i % rows, j % cols]
    return (v + i // rows + j // cols - 1) % 9 + 1


def solve(scale):
    solved, unsolved = {}, defaultdict(lambda: 9999)
    unsolved[(0, 0)] = 0
    target = (rows*scale-1, cols*scale-1)
    while target not in solved:
        dijkstra(solved, unsolved, scale)
    return solved[target]


def part1(): return solve(1)
def part2(): return solve(5)


print(part1())  # 720
print(part2())  # 3025

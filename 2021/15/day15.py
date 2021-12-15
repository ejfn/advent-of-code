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


def dijkstra(v: dict, u: dict, scale):
    k = min(u, key=u.get)
    v[k] = u[k]
    del u[k]
    for adj in find_adjs(k[0], k[1], scale):
        if adj in v:
            continue
        u[adj] = min(v[k] + scaled_value(adj), u[adj])


def scaled_value(x):
    i, j = x
    v = arr[i % rows, j % cols]
    return (v + i // rows + j // cols - 1) % 9 + 1


def solve(scale):
    visited, unvisited = {}, defaultdict(lambda: 9999)
    unvisited[(0, 0)] = 0
    target = (rows*scale-1, cols*scale-1)
    while target not in visited:
        dijkstra(visited, unvisited, scale)
    return visited[target]


def part1(): return solve(1)
def part2(): return solve(5)


print(part1())  # 720
print(part2())  # 3025

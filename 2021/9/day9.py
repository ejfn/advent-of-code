import os
import sys

m = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        m.append([int(i) for i in line.strip()])

rows = len(m)
cols = len(m[0])


def find_adjs(i, j):
    pos = [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]
    return filter(lambda p: p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols, pos)


def part1():
    sum = 0
    for i in range(rows):
        for j in range(cols):
            if all(m[i][j] < m[p[0]][p[1]] for p in find_adjs(i, j)):
                sum += m[i][j] + 1
                j += 1
    return sum


def find_basin(i, j, basin):
    l = basin[-1]
    lv = m[l[0]][l[1]]
    adjs = find_adjs(i, j)
    for a in adjs:
        if a in basin:
            continue
        v = m[a[0]][a[1]]
        if v > lv and v < 9:
            basin.append(a)
            find_basin(a[0], a[1], basin)


def part2():
    bc = []
    for i in range(rows):
        for j in range(cols):
            if all(m[i][j] < m[p[0]][p[1]] for p in find_adjs(i, j)):
                b = [(i, j)]
                find_basin(i, j, b)
                bc.append(len(b))
                bc = sorted(bc, reverse=True)[0:3]
                j += 1
    return (bc[0] * bc[1] * bc[2])


print(part1())  # 514
print(part2())  # 1103130

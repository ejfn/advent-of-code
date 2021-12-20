from collections import defaultdict
import os
import sys
import re
import math
import numpy as np
import scipy.linalg as linalg

scanners = {}
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        line = line.strip()
        if line != '':
            m = re.match(r'\-{3} scanner (\d+) \-{3}', line)
            if m != None:
                id = int(m.group(1))
                scanners[id] = []
            else:
                scanners[len(scanners)-1].append(
                    tuple([int(i) for i in line.split(',')]))

total_scanners = len(scanners)


def rot_matrix(axis, angle):
    rad = math.radians(angle)
    return linalg.expm(np.cross(np.eye(3), axis / linalg.norm(axis) * rad))


up_rots = [rot_matrix([0, 1, 0], 0), rot_matrix([0, 1, 0], 90),
           rot_matrix([0, 1, 0], 180), rot_matrix([0, 1, 0], 270)]
faces = [
    rot_matrix([1, 0, 0], 0), rot_matrix([1, 0, 0], 180),  # up, down
    rot_matrix([1, 0, 0], 90), rot_matrix([1, 0, 0], 270),  # front, back
    rot_matrix([0, 0, 1], 90),  rot_matrix([0, 0, 1], 270)  # right, left
]

rotations = [[x, y] for x in up_rots for y in faces]


def rotate(pt, rot):
    p = pt
    for m in rot:
        p = m.dot(p)
    p = tuple([round(i) for i in p])
    return p


def overlap(l1, l2):
    offsets = defaultdict(lambda: 0)
    for i in l1:
        for j in l2:
            o = tuple(np.array(j) - np.array(i))
            offsets[o] += 1
    k = max(offsets, key=offsets.get)
    return k if offsets[k] >= 12 else None


coords = {0: (0, 0, 0)}
solved = {0: scanners[0]}


def find_overlap(index):
    lst1 = solved[index]
    for j in range(total_scanners):
        if j in solved:
            continue
        for rj in rotations:
            lst2 = [rotate(x, rj) for x in scanners[j]]
            offset = overlap(lst2, lst1)
            if offset != None:
                coords[j] = offset
                solved[j] = np.array(lst2) + offset
                find_overlap(j)
                break


def part1():
    find_overlap(0)
    all = {}
    for x in solved.values():
        for i in x:
            all[tuple(i)] = 1
    return len(all)


def part2():
    md = 0
    for x in range(0, total_scanners - 1):
        for y in range(x + 1, total_scanners):
            c1, c2 = coords[x], coords[y]
            d = abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])
            md = max(d, md)
    return md


print(part1())  # 392
print(part2())  # 13332

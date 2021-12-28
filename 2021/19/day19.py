from collections import defaultdict
from scipy.spatial.transform import Rotation as R
import os
import sys
import re
import numpy as np
import itertools as it

scanners = {}
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        line = line.strip()
        if line != '':
            m = re.match(r'\-{3} scanner (\d+) \-{3}', line)
            if m is not None:
                id = int(m.group(1))
                scanners[id] = []
            else:
                scanners[len(scanners)-1].append(
                    tuple([int(i) for i in line.split(',')]))

total_scanners = len(scanners)

euler_rots = {
    'y': [0, 90, 180, 270],
    'xy': [[x, y] for x in [90, 270] for y in [0, 90, 180, 270]],
    'zy': [[z, y] for z in [90, 180, 270] for y in [0, 90, 180, 270]]
}
rotations = [R.from_euler(seq, angle, degrees=True).as_matrix()
             for seq, angels in euler_rots.items() for angle in angels]


def rotate(pt, rot):
    return tuple([round(i) for i in rot.dot(pt)])


def overlap(l1, l2):
    offsets = defaultdict(lambda: 0)
    for i, j in it.product(l1, l2):
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
            if offset is not None:
                coords[j] = offset
                solved[j] = np.array(lst2) + offset
                find_overlap(j)
                break


def part1():
    find_overlap(0)
    all = set([tuple(i) for x in solved.values() for i in x])
    print(len(all))


def part2():
    md = 0
    for x, y in it.combinations(range(total_scanners - 1), 2):
        c1, c2 = coords[x], coords[y]
        d = abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2])
        md = max(d, md)
    print(md)


part1()  # 392
part2()  # 13332

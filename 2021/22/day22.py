import os
import sys
import re
import itertools


def parse_line(line):
    m = re.match(
        r'(on|off) x=([-0-9]+)..([-0-9]+),y=([-0-9]+)..([-0-9]+),z=([-0-9]+)..([-0-9]+)', line)  # noqa
    return (m.group(1), [int(i) for i in m.group(2, 3, 4, 5, 6, 7)])


def part1():
    target = set(range(-50, 51))
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        result = set()
        for line in f:
            cmd, cube = parse_line(line)
            xx = set(range(cube[0], cube[1] + 1)) & target
            yy = set(range(cube[2], cube[3] + 1)) & target
            zz = set(range(cube[4], cube[5] + 1)) & target
            if len(xx) == 0 or len(yy) == 0 or len(zz) == 0:
                continue
            pts = set(itertools.product(xx, yy, zz))
            if cmd == 'on':
                result |= pts
            else:
                result -= pts
        print(len(result))


def intersect(a, b):
    x1, x2 = max(a[0], b[0]), min(a[1], b[1])
    y1, y2 = max(a[2], b[2]), min(a[3], b[3])
    z1, z2 = max(a[4], b[4]), min(a[5], b[5])
    if x1 <= x2 and y1 <= y2 and z1 <= z2:
        return x1, x2, y1, y2, z1, z2


def volume(c):
    x1, x2, y1, y2, z1, z2 = c
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def part2():
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        # using list here to help understanding, dict would be faster
        cubes = []
        for line in f:
            cmd, cube = parse_line(line)
            new_cubes = []
            for c, s in cubes:
                inter = intersect(cube, c)
                if inter:
                    new_cubes.append((inter, -1 if s > 0 else 1))
            if cmd == 'on':
                new_cubes.append((cube, 1))
            cubes += new_cubes
    total = sum(volume(c) * s for c, s in cubes)
    print(total)


part1()  # 580098
part2()  # 1134725012490723

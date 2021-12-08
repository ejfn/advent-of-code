import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r', encoding='utf-8') as f:
    lines = f.readlines()
half = len(lines) / 2


def part1():
    count = [0] * 12
    for line in lines:
        for i in range(12):
            count[i] += 1 if line[i] == '1' else 0

    x, y = '', ''
    for c in count:
        if c >= half:
            x += '1'
            y += '0'
        else:
            x += '0'
            y += '1'
    return int(x, 2) * int(y, 2)


def part2():
    t1 = lines
    for i in range(12):
        sp0 = [*filter(lambda s: s[i] == '0', t1)]
        sp1 = [*filter(lambda s: s[i] == '1', t1)]
        t1 = sp1 if len(sp0) <= len(sp1) else sp0
        if len(t1) == 1:
            break

    t2 = lines
    for i in range(12):
        sp0 = [*filter(lambda s: s[i] == '0', t2)]
        sp1 = [*filter(lambda s: s[i] == '1', t2)]
        t2 = sp0 if len(sp0) <= len(sp1) else sp1
        if len(t2) == 1:
            break
    return int(t1[0], 2) * int(t2[0], 2)


print(part1())
print(part2())

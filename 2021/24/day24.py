import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = f.readlines()

vars = []
for idx in range(14):
    i = int(lines[idx * 18 + 4].strip().split()[-1])
    j = int(lines[idx * 18 + 5].strip().split()[-1])
    k = int(lines[idx * 18 + 15].strip().split()[-1])
    vars.append((i, j, k))

numbers = range(9, 0, -1)


def solve(idx=0, z=0, result=[]):
    """See the analysis.xlsx to understand the solution."""
    if idx == 14:
        return ''.join([str(i) for i in result])
    a, b, c = vars[idx]
    if a == 26:
        chk = z % 26 + b
        z = z // a
        if 1 <= chk <= 9:
            return solve(idx + 1, z, result + [chk, ])
        return None
    for w in numbers:
        zz = z // a * 26 + w + c
        r = solve(idx + 1, zz, result + [w, ])
        if r is None:
            continue
        return r


def part1():
    print(solve())


def part2():
    global numbers
    numbers = range(1, 10)
    print(solve())


part1()  # 99799212949967
part2()  # 34198111816311

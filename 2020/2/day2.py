import os
import sys
import re

passwords = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        m = re.match('(\d+)-(\d+)\s([a-z]):\s([a-z]+)', line)
        passwords.append((int(m.group(1)), int(
            m.group(2)), m.group(3), m.group(4)))


def part1():
    print(sum([m <= len(re.findall(c, s)) <= n for m, n, c, s in passwords]))


def part2():
    print(sum([(s[m-1] == c) ^ (s[n-1] == c) for m, n, c, s in passwords]))


part1()  # 560
part2()  # 303

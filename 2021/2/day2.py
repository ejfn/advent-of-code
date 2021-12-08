import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    steps = [tuple(line.split()) for line in f]


def part1():
    pos, depth = 0, 0
    for x, y in steps:
        y = int(y)
        if x == 'forward':
            pos += y
        elif x == 'down':
            depth += y
        elif x == 'up':
            depth -= y
    return pos * depth


def part2():
    pos, depth, aim = 0, 0, 0
    for x, y in steps:
        y = int(y)
        if x == 'forward':
            pos += y
            depth += y * aim
        elif x == 'down':
            aim += y
        elif x == 'up':
            aim -= y
    return pos * depth


print(part1())
print(part2())

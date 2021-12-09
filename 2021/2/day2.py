import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    steps = [tuple(line.split()) for line in f]


def part1():
    pos, depth = 0, 0
    for x, y in steps:
        y = int(y)
        match x:
            case 'forward': pos += y
            case 'down': depth += y
            case 'up': depth -= y
    return pos * depth


def part2():
    pos, depth, aim = 0, 0, 0
    for x, y in steps:
        y = int(y)
        match x:
            case 'forward':
                pos += y
                depth += y * aim
            case 'down': aim += y
            case 'up': aim -= y
    return pos * depth


print(part1())  # 1484118
print(part2())  # 1463827010

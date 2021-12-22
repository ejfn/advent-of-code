from collections import defaultdict
import itertools
import os
import sys

entries = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        entries.append([i.split() for i in line.split('|')])


def part1():
    print(sum(1 for s in itertools.chain(*map(lambda x: x[1], entries))
              if len(s) in [2, 4, 3, 7]))


def determine(input, base):
    match len(input):
        case 2: return 1
        case 3: return 7
        case 4: return 4
        case 7: return 8
        case 5:
            if all(i in input for i in base[1]):
                return 3
            elif len(list(filter(lambda i: i not in base[4] + base[7], input))) == 1:
                return 5
            else:
                return 2
        case 6:
            if any(i not in input for i in base[1]):
                return 6
            elif len(list(filter(lambda i: i not in base[4] + base[7], input))) == 1:
                return 9
            else:
                return 0


def part2():
    sum = 0
    for e in entries:
        base = defaultdict()
        for i in filter(lambda i: len(i) in [2, 3, 4, 7], e[0]):
            base[determine(i, base)] = i
        for i in range(4):
            input = e[1][i]
            sum += 10 ** (3-i) * determine(input, base)
    print(sum)


part1()  # 421
part2()  # 986163

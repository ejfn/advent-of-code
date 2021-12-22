from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    arr = [[i for i in line.strip().split('-')] for line in f]

map = defaultdict(lambda: [])
for i, j in arr:
    if i == 'start':  # no back to start
        map[i] += [j]
    elif j == 'start':  # no back to start
        map[j] += [i]
    else:
        map[i] += [j]
        map[j] += [i]


def traverse(cave, visited, is_part1):
    if cave == 'end':
        return 1
    is_repeat = False
    if str.islower(cave[0]) and visited[cave] > 0:
        if is_part1 or visited['_'] == 1:
            return 0
        else:
            visited['_'] = 1  # flag it
            is_repeat = True
    visited[cave] += 1
    sum = 0
    for n in map[cave]:
        sum += traverse(n, visited, is_part1)
    visited[cave] -= 1
    if is_repeat:
        visited['_'] = 0
    return sum


def part1(): print(traverse('start', defaultdict(lambda: 0), True))
def part2(): print(traverse('start', defaultdict(lambda: 0), False))


part1()  # 4691
part2()  # 140718

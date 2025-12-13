import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

MFCSAM = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

def parse_sues(lines):
    sues = {}
    for line in lines:
        m = re.match(r'Sue (\d+): (.+)', line)
        sue_num = int(m.group(1))
        things = {}
        for item in m.group(2).split(', '):
            name, count = item.split(': ')
            things[name] = int(count)
        sues[sue_num] = things
    return sues

def part1(lines):
    sues = parse_sues(lines)
    for sue_num, things in sues.items():
        if all(MFCSAM[k] == v for k, v in things.items()):
            return sue_num
    return None

def part2(lines):
    sues = parse_sues(lines)
    for sue_num, things in sues.items():
        match = True
        for k, v in things.items():
            if k in ('cats', 'trees'):
                if v <= MFCSAM[k]:
                    match = False
                    break
            elif k in ('pomeranians', 'goldfish'):
                if v >= MFCSAM[k]:
                    match = False
                    break
            else:
                if v != MFCSAM[k]:
                    match = False
                    break
        if match:
            return sue_num
    return None

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

import os
import sys
import re

# Load input from input.txt in same directory as script
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    line = f.read().strip()

# Parse rotations: e.g., "L68,L30,R48" -> [('L', 68), ('L', 30), ('R', 48)]
rotations = []
for match in re.finditer(r'([LR])(\d+)', line):
    rotations.append((match.group(1), int(match.group(2))))

def part1():
    pos = 50  # Starting position
    count = 0
    for direction, dist in rotations:
        if direction == 'R':
            pos = (pos + dist) % 100
        else:  # 'L'
            pos = (pos - dist) % 100
        if pos == 0:
            count += 1
    print(count)  # Password: times at 0
    return count

def count_during(pos, direction, dist):
    if dist == 0:
        return 0
    dir_val = 1 if direction == 'R' else -1
    if dir_val == 1:
        step = (-pos % 100)
        if step == 0:
            step = 100
    else:
        step = (pos % 100)
        if step == 0:
            step = 100
    if step > dist:
        return 0
    return (dist - step) // 100 + 1


def part2():
    pos = 50
    total = 0
    for direction, dist in rotations:
        hits = count_during(pos, direction, dist)
        total += hits
        if direction == 'R':
            pos = (pos + dist) % 100
        else:
            pos = (pos - dist) % 100
    print(total)  # New password: total hits at 0 during all rotations
    return total

part1()
part2()

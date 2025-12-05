import os
import sys

# Load input from input.txt in same directory as script
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    line = f.read().strip()

# Parse ranges: e.g., "11-22,95-115" -> [(11,22), (95,115)]
ranges = []
for part in line.split(','):
    low, high = map(int, part.split('-'))
    ranges.append((low, high))

def is_invalid_id(n):
    s = str(n)
    if len(s) % 2 != 0 or s[0] == '0':
        return False
    half = len(s) // 2
    return s[:half] == s[half:]

def part1():
    total = 0
    for low, high in ranges:
        for num in range(low, high + 1):
            if is_invalid_id(num):
                total += num
    print(total)  # Sum of invalid IDs
    return total

def is_invalid_part2(n):
    s = str(n)
    if s[0] == '0':
        return False
    l = len(s)
    for d in range(1, l // 2 + 1):
        if l % d == 0:
            k = l // d
            if k >= 2:
                chunk = s[:d]
                if all(s[i*d:(i+1)*d] == chunk for i in range(1, k)):
                    return True
    return False


def part2():
    total = 0
    for low, high in ranges:
        for num in range(low, high + 1):
            if is_invalid_part2(num):
                total += num
    print(total)  # Sum of invalid IDs with >=2 repetitions
    return total

part1()
part2()

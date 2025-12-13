import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def is_nice_part1(s):
    # At least 3 vowels
    vowels = sum(1 for c in s if c in 'aeiou')
    if vowels < 3:
        return False
    # Double letter
    if not re.search(r'(.)\1', s):
        return False
    # No forbidden strings
    if any(bad in s for bad in ['ab', 'cd', 'pq', 'xy']):
        return False
    return True

def is_nice_part2(s):
    # Pair of two letters appearing twice without overlap
    if not re.search(r'(..).*\1', s):
        return False
    # Letter repeating with exactly one letter between
    if not re.search(r'(.).\1', s):
        return False
    return True

def part1(strings):
    return sum(1 for s in strings if is_nice_part1(s))

def part2(strings):
    return sum(1 for s in strings if is_nice_part2(s))

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

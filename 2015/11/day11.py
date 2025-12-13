import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def increment_password(pw):
    pw = list(pw)
    i = len(pw) - 1
    while i >= 0:
        if pw[i] == 'z':
            pw[i] = 'a'
            i -= 1
        else:
            pw[i] = chr(ord(pw[i]) + 1)
            break
    return ''.join(pw)

def has_straight(pw):
    for i in range(len(pw) - 2):
        if ord(pw[i+1]) == ord(pw[i]) + 1 and ord(pw[i+2]) == ord(pw[i]) + 2:
            return True
    return False

def no_confusing_letters(pw):
    return not any(c in pw for c in 'iol')

def has_two_pairs(pw):
    pairs = re.findall(r'(.)\1', pw)
    return len(set(pairs)) >= 2

def is_valid(pw):
    return has_straight(pw) and no_confusing_letters(pw) and has_two_pairs(pw)

def next_valid_password(pw):
    pw = increment_password(pw)
    # Skip confusing letters early for efficiency
    for i, c in enumerate(pw):
        if c in 'iol':
            pw = pw[:i] + chr(ord(c) + 1) + 'a' * (len(pw) - i - 1)
            break
    while not is_valid(pw):
        pw = increment_password(pw)
        for i, c in enumerate(pw):
            if c in 'iol':
                pw = pw[:i] + chr(ord(c) + 1) + 'a' * (len(pw) - i - 1)
                break
    return pw

def part1(pw):
    return next_valid_password(pw)

def part2(pw):
    return next_valid_password(next_valid_password(pw))

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

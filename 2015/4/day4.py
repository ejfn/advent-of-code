import os
import sys
import hashlib

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def find_hash(secret, prefix):
    i = 1
    while True:
        h = hashlib.md5(f"{secret}{i}".encode()).hexdigest()
        if h.startswith(prefix):
            return i
        i += 1

def part1(secret):
    return find_hash(secret, '00000')

def part2(secret):
    return find_hash(secret, '000000')

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

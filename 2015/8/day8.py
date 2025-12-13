import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def code_len(s):
    return len(s)

def memory_len(s):
    # Remove surrounding quotes
    inner = s[1:-1]
    count = 0
    i = 0
    while i < len(inner):
        if inner[i] == '\\':
            if inner[i+1] in '\\"':
                count += 1
                i += 2
            elif inner[i+1] == 'x':
                count += 1
                i += 4
            else:
                count += 1
                i += 1
        else:
            count += 1
            i += 1
    return count

def encoded_len(s):
    # Encode: surround with quotes, escape \ and "
    result = '"'
    for c in s:
        if c == '\\':
            result += '\\\\'
        elif c == '"':
            result += '\\"'
        else:
            result += c
    result += '"'
    return len(result)

def part1(strings):
    return sum(code_len(s) - memory_len(s) for s in strings)

def part2(strings):
    return sum(encoded_len(s) - code_len(s) for s in strings)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

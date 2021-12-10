import os
import sys
import math

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = f.readlines()

pair = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

score_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def part1():
    sum = 0
    for line in lines:
        stack = []
        for c in line.strip():
            if c in pair:
                if len(stack) == 0 or stack.pop() != pair[c]:
                    sum += score_map[c]
                    break
            else:
                stack.append(c)
    return sum


score_map_2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def part2():
    scores = []
    for line in lines:
        stack = []
        for c in line.strip():
            if c in pair:
                if len(stack) == 0 or stack.pop() != pair[c]:
                    stack.clear()
                    break
            else:
                stack.append(c)
        if len(stack) > 0:
            sum = 0
            while len(stack) > 0:
                p = stack.pop()
                sum = sum * 5 + score_map_2[p]
            scores.append(sum)
    return sorted(scores)[math.floor(len(scores) / 2)]


print(part1())  # 339537
print(part2())  # 2412013412

import os
import sys

# Load input from input.txt in same directory as script
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    banks = [line.strip() for line in f.readlines() if line.strip()]


def part1():
    total = 0
    for bank in banks:
        max_jolt = 0
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                jolt = int(bank[i] + bank[j])
                if jolt > max_jolt:
                    max_jolt = jolt
        total += max_jolt
    print(total)  # Total joltage
    return total


def largest_k_digits(s, k):
    n = len(s)
    if n <= k:
        return s
    to_remove = n - k
    stack = []
    for digit in s:
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    # Remove remaining from end if needed
    while to_remove > 0:
        if stack:
            stack.pop()
        to_remove -= 1
    return ''.join(stack)


def part2():
    total = 0
    for bank in banks:
        sub = largest_k_digits(bank, 12)
        total += int(sub)
    print(total)  # Total joltage with 12 batteries per bank
    return total


part1()
part2()

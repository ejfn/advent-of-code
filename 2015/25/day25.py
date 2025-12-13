import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        text = f.read().strip()
    # Extract row and column from the message
    m = re.search(r'row (\d+)', text)
    row = int(m.group(1))
    m = re.search(r'column (\d+)', text)
    col = int(m.group(1))
    return row, col

def get_index(row, col):
    # The index at (row, col) in the diagonal fill pattern
    # First, get to diagonal (row + col - 1)
    # Then count within that diagonal
    diag = row + col - 1
    # Number of elements in all previous diagonals
    total_before = diag * (diag - 1) // 2
    # Position within this diagonal (0-indexed from top)
    return total_before + col

def get_code(index):
    code = 20151125
    for _ in range(index - 1):
        code = (code * 252533) % 33554393
    return code

def part1(row, col):
    idx = get_index(row, col)
    return get_code(idx)

if __name__ == "__main__":
    row, col = load_input()
    print("Part 1:", part1(row, col))
    # Day 25 only has Part 1
    print("Part 2: (no Part 2 on Day 25)")

import sys
import os
from collections import Counter

def solve_part1(lines):
    if not lines:
        return ""
    
    cols = len(lines[0].strip())
    message = []
    
    for i in range(cols):
        col_chars = [line[i] for line in lines if len(line) > i]
        c = Counter(col_chars)
        most_common = c.most_common(1)[0][0]
        message.append(most_common)
        
    return "".join(message)

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return solve_part1(lines)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    if not lines:
        return ""
    
    cols = len(lines[0])
    message = []
    
    for i in range(cols):
        col_chars = [line[i] for line in lines if len(line) > i]
        c = Counter(col_chars)
        # least common is the last element in most_common()
        least_common = c.most_common()[-1][0]
        message.append(least_common)
        
    return "".join(message)

def run_example():
    example = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""
    lines = [l.strip() for l in example.splitlines()]
    print(f"Example Part 1: {solve_part1(lines)} (expected easter)")

if __name__ == "__main__":
    print("Testing example:")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())

import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_instruction(line):
    m = re.match(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)', line)
    action = m.group(1)
    x1, y1, x2, y2 = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
    return action, x1, y1, x2, y2

def part1(instructions):
    grid = [[False] * 1000 for _ in range(1000)]
    for line in instructions:
        action, x1, y1, x2, y2 = parse_instruction(line)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if action == 'turn on':
                    grid[x][y] = True
                elif action == 'turn off':
                    grid[x][y] = False
                else:  # toggle
                    grid[x][y] = not grid[x][y]
    return sum(sum(row) for row in grid)

def part2(instructions):
    grid = [[0] * 1000 for _ in range(1000)]
    for line in instructions:
        action, x1, y1, x2, y2 = parse_instruction(line)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if action == 'turn on':
                    grid[x][y] += 1
                elif action == 'turn off':
                    grid[x][y] = max(0, grid[x][y] - 1)
                else:  # toggle
                    grid[x][y] += 2
    return sum(sum(row) for row in grid)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

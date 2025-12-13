import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def part1(moves):
    x, y = 0, 0
    visited = {(0, 0)}
    for c in moves:
        if c == '^': y += 1
        elif c == 'v': y -= 1
        elif c == '>': x += 1
        elif c == '<': x -= 1
        visited.add((x, y))
    return len(visited)

def part2(moves):
    positions = [[0, 0], [0, 0]]  # Santa and Robo-Santa
    visited = {(0, 0)}
    for i, c in enumerate(moves):
        pos = positions[i % 2]
        if c == '^': pos[1] += 1
        elif c == 'v': pos[1] -= 1
        elif c == '>': pos[0] += 1
        elif c == '<': pos[0] -= 1
        visited.add(tuple(pos))
    return len(visited)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

import os
import sys


# Cube coordinates for hex grid
# https://www.redblobgames.com/grids/hexagons/
DIRS = {
    'n':  (0, 1, -1),
    'ne': (1, 0, -1),
    'se': (1, -1, 0),
    's':  (0, -1, 1),
    'sw': (-1, 0, 1),
    'nw': (-1, 1, 0),
}


def hex_distance(x, y, z):
    """Distance from origin in cube coordinates."""
    return (abs(x) + abs(y) + abs(z)) // 2


def solve(steps):
    """Returns (final distance, max distance ever)."""
    x, y, z = 0, 0, 0
    max_dist = 0
    
    for step in steps:
        dx, dy, dz = DIRS[step]
        x += dx
        y += dy
        z += dz
        max_dist = max(max_dist, hex_distance(x, y, z))
    
    return hex_distance(x, y, z), max_dist


def part1(steps):
    return solve(steps)[0]


def part2(steps):
    return solve(steps)[1]


def run_example():
    assert part1("ne,ne,ne".split(',')) == 3
    assert part1("ne,ne,sw,sw".split(',')) == 0
    assert part1("ne,ne,s,s".split(',')) == 2
    assert part1("se,sw,se,sw,sw".split(',')) == 3
    print("Part 1 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        steps = f.read().strip().split(',')
    
    print(f"Part 1: {part1(steps)}")
    print(f"Part 2: {part2(steps)}")

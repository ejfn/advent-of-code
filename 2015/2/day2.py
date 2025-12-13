import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [list(map(int, line.strip().split('x'))) for line in f if line.strip()]

def part1(boxes):
    total = 0
    for l, w, h in boxes:
        sides = [l*w, w*h, h*l]
        total += 2 * sum(sides) + min(sides)
    return total

def part2(boxes):
    total = 0
    for dims in boxes:
        dims = sorted(dims)
        ribbon = 2 * (dims[0] + dims[1])
        bow = dims[0] * dims[1] * dims[2]
        total += ribbon + bow
    return total

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

import os
import sys
from typing import List, Tuple

Instruction = Tuple[str, int]


def parse(data: str) -> List[Instruction]:
    instructions: List[Instruction] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        instructions.append((line[0], int(line[1:])))
    return instructions


def rotate(x: int, y: int, degrees: int) -> Tuple[int, int]:
    degrees %= 360
    if degrees == 0:
        return x, y
    if degrees == 90:
        return y, -x
    if degrees == 180:
        return -x, -y
    if degrees == 270:
        return -y, x
    raise ValueError('Invalid rotation')


def part1(data: str) -> int:
    instructions = parse(data)
    x = y = 0
    dir_x, dir_y = 1, 0  # east
    for action, value in instructions:
        if action == 'N':
            y += value
        elif action == 'S':
            y -= value
        elif action == 'E':
            x += value
        elif action == 'W':
            x -= value
        elif action == 'L':
            dir_x, dir_y = rotate(dir_x, dir_y, -value % 360)
        elif action == 'R':
            dir_x, dir_y = rotate(dir_x, dir_y, value)
        elif action == 'F':
            x += dir_x * value
            y += dir_y * value
        else:
            raise ValueError('Unknown action')
    return abs(x) + abs(y)


def part2(data: str) -> int:
    instructions = parse(data)
    ship_x = ship_y = 0
    wp_x, wp_y = 10, 1
    for action, value in instructions:
        if action == 'N':
            wp_y += value
        elif action == 'S':
            wp_y -= value
        elif action == 'E':
            wp_x += value
        elif action == 'W':
            wp_x -= value
        elif action == 'L':
            wp_x, wp_y = rotate(wp_x, wp_y, -value % 360)
        elif action == 'R':
            wp_x, wp_y = rotate(wp_x, wp_y, value)
        elif action == 'F':
            ship_x += wp_x * value
            ship_y += wp_y * value
        else:
            raise ValueError('Unknown action')
    return abs(ship_x) + abs(ship_y)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """F10\nN3\nF7\nR90\nF11"""
    print("Example Part 1:", part1(example))  # Expected 25
    print("Example Part 2:", part2(example))  # Expected 286


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

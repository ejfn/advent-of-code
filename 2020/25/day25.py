import os
import sys
from typing import Tuple

MOD = 20201227
SUBJECT = 7


def parse(data: str) -> Tuple[int, int]:
    lines = [int(line) for line in data.splitlines() if line.strip()]
    return lines[0], lines[1]


def find_loop_size(public_key: int) -> int:
    value = 1
    loop = 0
    while value != public_key:
        value = (value * SUBJECT) % MOD
        loop += 1
    return loop


def transform(subject: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = (value * subject) % MOD
    return value


def part1(data: str) -> int:
    card_key, door_key = parse(data)
    card_loop = find_loop_size(card_key)
    return transform(door_key, card_loop)


def part2(_: str) -> str:
    return 'Merry Christmas!'


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """5764801\n17807724"""
    print("Example Part 1:", part1(example))  # Expected 14897079


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

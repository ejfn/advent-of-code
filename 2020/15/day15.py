import os
import sys
from typing import List


def parse(data: str) -> List[int]:
    return [int(x) for x in data.strip().split(',')]


def play(numbers: List[int], target: int) -> int:
    last_seen = {num: idx + 1 for idx, num in enumerate(numbers[:-1])}
    current = numbers[-1]
    turn = len(numbers)
    while turn < target:
        previous = last_seen.get(current)
        last_seen[current] = turn
        if previous is None:
            current = 0
        else:
            current = turn - previous
        turn += 1
    return current


def part1(data: str) -> int:
    return play(parse(data), 2020)


def part2(data: str) -> int:
    return play(parse(data), 30000000)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = "0,3,6"
    print("Example Part 1:", part1(example))  # Expected 436
    print("Example Part 2:", part2(example))  # Expected 175594


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

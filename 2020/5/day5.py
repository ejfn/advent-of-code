import os
import sys
from typing import List


def parse(data: str) -> List[str]:
    return [line.strip() for line in data.splitlines() if line.strip()]


def seat_id(code: str) -> int:
    binary = code.translate(str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'}))
    return int(binary, 2)


def part1(data: str) -> int:
    ids = [seat_id(code) for code in parse(data)]
    return max(ids)


def part2(data: str) -> int:
    ids = sorted(seat_id(code) for code in parse(data))
    for prev, curr in zip(ids, ids[1:]):
        if curr - prev == 2:
            return curr - 1
    raise RuntimeError('Seat not found')


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """BFFFBBFRRR\nFFFBBBFRRR\nBBFFBBFRLL"""
    print("Example Part 1:", part1(example))  # Expected 820


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

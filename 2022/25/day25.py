import os
import sys
from typing import List

SNAFU_TO_INT = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
INT_TO_SNAFU = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}


def snafu_to_decimal(value: str) -> int:
    total = 0
    for ch in value:
        total = total * 5 + SNAFU_TO_INT[ch]
    return total


def decimal_to_snafu(number: int) -> str:
    if number == 0:
        return '0'
    digits: List[str] = []
    n = number
    while n:
        n, rem = divmod(n, 5)
        if rem <= 2:
            digits.append(INT_TO_SNAFU[rem])
        else:
            digits.append(INT_TO_SNAFU[rem])
            n += 1
    return ''.join(reversed(digits))


def parse(data: str) -> List[str]:
    return [line.strip() for line in data.splitlines() if line.strip()]


def part1(data: str) -> str:
    numbers = parse(data)
    total = sum(snafu_to_decimal(value) for value in numbers)
    return decimal_to_snafu(total)


def part2(_: str) -> str:
    return "Merry Christmas!"


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """1=-0-2\n12111\n2=0=\n21\n2=01\n111\n20012\n112\n1=-1=\n1-12\n12\n1=\n122"""
    print("Example Part 1:", part1(example))  # Expected 2=-1=0


if __name__ == "__main__":
    data = read_input()
    print(part1(data))
    print(part2(data))

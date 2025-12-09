import os
import sys
from typing import List


def parse_groups(data: str) -> List[List[str]]:
    groups: List[List[str]] = []
    for block in data.strip().split('\n\n'):
        groups.append([line.strip() for line in block.splitlines() if line.strip()])
    return groups


def part1(data: str) -> int:
    groups = parse_groups(data)
    return sum(len(set().union(*map(set, group))) for group in groups)


def part2(data: str) -> int:
    groups = parse_groups(data)
    total = 0
    for group in groups:
        common = set(group[0])
        for person in group[1:]:
            common &= set(person)
        total += len(common)
    return total


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """abc\n\na\n b\n c\n\nab\n ac\n\na\n a\n a\n a\n\nb""".replace(' ', '')
    print("Example Part 1:", part1(example))  # Expected 11
    print("Example Part 2:", part2(example))  # Expected 6


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

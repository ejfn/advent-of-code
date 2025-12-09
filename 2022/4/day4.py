import os
import sys
from typing import Iterable


def parse(data: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    pairs = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        left, right = line.split(",")
        a1, a2 = map(int, left.split("-"))
        b1, b2 = map(int, right.split("-"))
        pairs.append(((a1, a2), (b1, b2)))
    return pairs


def contains(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] and a[1] >= b[1]


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def part1(data: str) -> int:
    return sum(
        contains(a, b) or contains(b, a)
        for a, b in parse(data)
    )


def part2(data: str) -> int:
    return sum(overlaps(a, b) for a, b in parse(data))


def run_example() -> None:
    example = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    assert part1(example) == 2
    assert part2(example) == 4
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

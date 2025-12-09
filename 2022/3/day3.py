import os
import sys
from textwrap import dedent


def priority(ch: str) -> int:
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 1
    return ord(ch) - ord("A") + 27


def parse(data: str) -> list[str]:
    return [line.strip() for line in data.strip().splitlines() if line.strip()]


def part1(data: str) -> int:
    total = 0
    for line in parse(data):
        mid = len(line) // 2
        left = set(line[:mid])
        right = set(line[mid:])
        common = (left & right).pop()
        total += priority(common)
    return total


def part2(data: str) -> int:
    lines = parse(data)
    total = 0
    for i in range(0, len(lines), 3):
        group = lines[i : i + 3]
        badge = set(group[0]) & set(group[1]) & set(group[2])
        total += priority(next(iter(badge)))
    return total


def run_example() -> None:
    example = dedent(
        """\
        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """
    )
    assert part1(example) == 157
    assert part2(example) == 70
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

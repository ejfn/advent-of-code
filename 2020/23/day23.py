import os
import sys
from typing import List, Optional


def parse(data: str) -> List[int]:
    return [int(ch) for ch in data.strip()]


def play(labels: List[int], moves: int, total: Optional[int] = None) -> List[int]:
    if total is None:
        total = len(labels)
    max_label = max(total, max(labels))
    next_cup = [0] * (max_label + 1)
    prev = labels[0]
    for label in labels[1:]:
        next_cup[prev] = label
        prev = label
    if total > len(labels):
        for label in range(max(labels) + 1, total + 1):
            next_cup[prev] = label
            prev = label
        max_label = total
    next_cup[prev] = labels[0]
    current = labels[0]
    for _ in range(moves):
        pick1 = next_cup[current]
        pick2 = next_cup[pick1]
        pick3 = next_cup[pick2]
        picked = {pick1, pick2, pick3}
        next_cup[current] = next_cup[pick3]
        dest = current - 1 if current > 1 else max_label
        while dest in picked:
            dest -= 1
            if dest == 0:
                dest = max_label
        next_cup[pick3] = next_cup[dest]
        next_cup[dest] = pick1
        current = next_cup[current]
    return next_cup


def part1(data: str) -> str:
    labels = parse(data)
    next_cup = play(labels, 100)
    result: List[str] = []
    value = next_cup[1]
    while value != 1:
        result.append(str(value))
        value = next_cup[value]
    return ''.join(result)


def part2(data: str) -> int:
    labels = parse(data)
    next_cup = play(labels, 10_000_000, total=1_000_000)
    first = next_cup[1]
    second = next_cup[first]
    return first * second


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = "389125467"
    print("Example Part 1:", part1(example))  # Expected 67384529
    print("Example Part 2:", part2(example))  # Expected 149245887792


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

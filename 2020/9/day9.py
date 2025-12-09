import os
import sys
from typing import List

PREAMBLE = 25


def parse(data: str) -> List[int]:
    return [int(line) for line in data.splitlines() if line.strip()]


def find_invalid(numbers: List[int], preamble: int = PREAMBLE) -> int:
    for i in range(preamble, len(numbers)):
        target = numbers[i]
        window = numbers[i - preamble:i]
        seen = set()
        valid = False
        for num in window:
            if target - num in seen:
                valid = True
                break
            seen.add(num)
        if not valid:
            return target
    raise RuntimeError('All numbers valid')


def find_weakness(numbers: List[int], target: int) -> int:
    start = 0
    current = 0
    for end, value in enumerate(numbers):
        current += value
        while current > target and start < end:
            current -= numbers[start]
            start += 1
        if current == target and end - start >= 1:
            contiguous = numbers[start:end + 1]
            return min(contiguous) + max(contiguous)
    raise RuntimeError('No range found')


def part1(data: str) -> int:
    numbers = parse(data)
    return find_invalid(numbers)


def part2(data: str) -> int:
    numbers = parse(data)
    invalid = find_invalid(numbers)
    return find_weakness(numbers, invalid)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    print("Example Part 1:", find_invalid(parse(example), preamble=5))  # Expected 127
    print("Example Part 2:", find_weakness(parse(example), 127))  # Expected 62


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

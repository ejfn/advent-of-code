import os
import sys
from functools import lru_cache
from typing import List


def parse(data: str) -> List[int]:
    adapters = sorted(int(line) for line in data.splitlines() if line.strip())
    return adapters


def part1(data: str) -> int:
    adapters = parse(data)
    current = 0
    diff1 = diff3 = 0
    for rating in adapters:
        diff = rating - current
        if diff == 1:
            diff1 += 1
        elif diff == 3:
            diff3 += 1
        elif diff == 2:
            pass
        else:
            raise ValueError('Invalid difference')
        current = rating
    diff3 += 1  # device
    return diff1 * diff3


def part2(data: str) -> int:
    adapters = [0] + parse(data)
    device = adapters[-1] + 3
    adapters.append(device)
    adapter_set = set(adapters)

    @lru_cache(maxsize=None)
    def ways(value: int) -> int:
        if value == device:
            return 1
        total = 0
        for delta in (1, 2, 3):
            nxt = value + delta
            if nxt in adapter_set:
                total += ways(nxt)
        return total

    return ways(0)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """16
10
15
5
1
11
7
19
6
12
4"""
    print("Example Part 1:", part1(example))  # Expected 35
    print("Example Part 2:", part2(example))  # Expected 8


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

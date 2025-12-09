import os
import sys
from math import gcd
from typing import List, Tuple


def parse(data: str) -> Tuple[int, List[str]]:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    earliest = int(lines[0])
    schedule = lines[1].split(',')
    return earliest, schedule


def part1(data: str) -> int:
    earliest, schedule = parse(data)
    buses = [int(x) for x in schedule if x != 'x']
    best_bus = None
    best_wait = None
    for bus in buses:
        wait = (-earliest) % bus
        if best_wait is None or wait < best_wait:
            best_wait = wait
            best_bus = bus
    assert best_bus is not None and best_wait is not None
    return best_bus * best_wait


def part2(data: str) -> int:
    _, schedule = parse(data)
    offsets = [(int(bus), offset) for offset, bus in enumerate(schedule) if bus != 'x']
    timestamp = 0
    step = 1
    for bus, offset in offsets:
        while (timestamp + offset) % bus != 0:
            timestamp += step
        step = step * bus // gcd(step, bus)
    return timestamp


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """939
7,13,x,x,59,x,31,19"""
    print("Example Part 1:", part1(example))  # Expected 295
    print("Example Part 2:", part2(example))  # Expected 1068781


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

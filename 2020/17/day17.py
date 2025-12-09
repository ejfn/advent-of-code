import itertools
import os
import sys
from typing import List, Set, Tuple

Coordinate = Tuple[int, ...]


def parse(data: str) -> Set[Coordinate]:
    active: Set[Coordinate] = set()
    for y, line in enumerate(data.splitlines()):
        line = line.strip()
        if not line:
            continue
        for x, ch in enumerate(line):
            if ch == '#':
                active.add((x, y))
    return active


def build_offsets(dims: int) -> List[Coordinate]:
    offsets = []
    for delta in itertools.product((-1, 0, 1), repeat=dims):
        if all(d == 0 for d in delta):
            continue
        offsets.append(delta)
    return offsets


def run(data: str, dims: int) -> int:
    base_active = parse(data)
    active = {coord + (0,) * (dims - len(coord)) for coord in base_active}
    offsets = build_offsets(dims)
    for _ in range(6):
        neighbor_counts = {}
        for coord in active:
            for delta in offsets:
                neighbor = tuple(c + d for c, d in zip(coord, delta))
                neighbor_counts[neighbor] = neighbor_counts.get(neighbor, 0) + 1
        new_active = set()
        for coord, count in neighbor_counts.items():
            if coord in active and count in (2, 3):
                new_active.add(coord)
            elif coord not in active and count == 3:
                new_active.add(coord)
        active = new_active
    return len(active)


def part1(data: str) -> int:
    return run(data, 3)


def part2(data: str) -> int:
    return run(data, 4)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """.#.
..#
###"""
    print("Example Part 1:", part1(example))  # Expected 112
    print("Example Part 2:", part2(example))  # Expected 848


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

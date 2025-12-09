import os
import sys
from collections import Counter, deque
from typing import Deque, Set, Tuple

Position = Tuple[int, int]
NEIGHBOR_OFFSETS: Tuple[Position, ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)
DIRECTION_RULES: Tuple[Tuple[Position, Tuple[Position, Position, Position]], ...] = (
    ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),  # North
    ((1, 0), ((1, -1), (1, 0), (1, 1))),      # South
    ((0, -1), ((-1, -1), (0, -1), (1, -1))),  # West
    ((0, 1), ((-1, 1), (0, 1), (1, 1))),      # East
)


def parse(data: str) -> Set[Position]:
    elves: Set[Position] = set()
    for r, line in enumerate(data.splitlines()):
        for c, ch in enumerate(line):
            if ch == '#':
                elves.add((r, c))
    return elves


def simulate_round(elves: Set[Position], order: Deque[Tuple[Position, Tuple[Position, ...]]]) -> Tuple[Set[Position], bool]:
    proposals: dict[Position, Position] = {}
    counts: Counter[Position] = Counter()

    for r, c in elves:
        if not any((r + dr, c + dc) in elves for dr, dc in NEIGHBOR_OFFSETS):
            continue
        for delta, checks in order:
            if all((r + dr, c + dc) not in elves for dr, dc in checks):
                dest = (r + delta[0], c + delta[1])
                proposals[(r, c)] = dest
                counts[dest] += 1
                break

    new_elves: Set[Position] = set()
    moved = False
    for pos in elves:
        dest = proposals.get(pos)
        if dest and counts[dest] == 1:
            new_elves.add(dest)
            moved = True
        else:
            new_elves.add(pos)

    order.rotate(-1)
    return new_elves, moved


def empty_tiles(elves: Set[Position]) -> int:
    rows = [r for r, _ in elves]
    cols = [c for _, c in elves]
    area = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1)
    return area - len(elves)


def part1(data: str) -> int:
    elves = parse(data.strip())
    order: Deque[Tuple[Position, Tuple[Position, ...]]] = deque(DIRECTION_RULES)
    for _ in range(10):
        elves, _ = simulate_round(elves, order)
    return empty_tiles(elves)


def part2(data: str) -> int:
    elves = parse(data.strip())
    order: Deque[Tuple[Position, Tuple[Position, ...]]] = deque(DIRECTION_RULES)
    rounds = 0
    while True:
        rounds += 1
        elves, moved = simulate_round(elves, order)
        if not moved:
            return rounds


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
    print("Example Part 1:", part1(example))  # Expected 110
    print("Example Part 2:", part2(example))  # Expected 20


if __name__ == "__main__":
    data = read_input()
    print(part1(data))
    print(part2(data))

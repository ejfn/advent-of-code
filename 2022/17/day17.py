import os
import sys
from textwrap import dedent


ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]


def simulate(data: str, total_rocks: int) -> int:
    jets = data.strip()
    jet_len = len(jets)
    occupied = set()
    max_y = -1
    jet_index = 0
    column_heights = [-1] * 7
    seen = {}
    added_height = 0
    rock_count = 0
    skip_done = False

    def can_move(rock, dx, dy):
        for x, y in rock:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= 7 or ny < 0:
                return False
            if (nx, ny) in occupied:
                return False
        return True

    while rock_count < total_rocks:
        shape = ROCKS[rock_count % len(ROCKS)]
        rock = [(x + 2, y + max_y + 4) for x, y in shape]

        while True:
            jet = jets[jet_index % jet_len]
            jet_index = (jet_index + 1) % jet_len
            dx = -1 if jet == "<" else 1
            if can_move(rock, dx, 0):
                rock = [(x + dx, y) for x, y in rock]
            if can_move(rock, 0, -1):
                rock = [(x, y - 1) for x, y in rock]
            else:
                for x, y in rock:
                    occupied.add((x, y))
                    column_heights[x] = max(column_heights[x], y)
                max_y = max(max_y, max(y for _, y in rock))
                break

        rock_count += 1

        profile = tuple(max_y - column_heights[x] for x in range(7))
        key = (rock_count % len(ROCKS), jet_index, profile)
        if not skip_done:
            if key in seen:
                prev_rock, prev_height = seen[key]
                cycle_len = rock_count - prev_rock
                height_gain = max_y - prev_height
                remaining = total_rocks - rock_count
                if cycle_len > 0:
                    cycles = remaining // cycle_len
                    if cycles:
                        rock_count += cycles * cycle_len
                        added_height += cycles * height_gain
                        skip_done = True
            else:
                seen[key] = (rock_count, max_y)

    return max_y + 1 + added_height


def part1(data: str) -> int:
    return simulate(data, 2022)


def part2(data: str) -> int:
    return simulate(data, 1_000_000_000_000)


def run_example() -> None:
    test_jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    assert part1(test_jets) == 3068
    assert part2(test_jets) == 1514285714288
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

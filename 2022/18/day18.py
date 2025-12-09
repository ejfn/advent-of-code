import os
import sys
from collections import deque
from textwrap import dedent


DIRECTIONS = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def parse(data: str) -> set[tuple[int, int, int]]:
    cubes = set()
    for line in data.strip().splitlines():
        cubes.add(tuple(map(int, line.split(","))))
    return cubes


def part1(data: str) -> int:
    cubes = parse(data)
    surface = 0
    for x, y, z in cubes:
        for dx, dy, dz in DIRECTIONS:
            if (x + dx, y + dy, z + dz) not in cubes:
                surface += 1
    return surface


def part2(data: str) -> int:
    cubes = parse(data)
    min_x = min(x for x, _, _ in cubes) - 1
    max_x = max(x for x, _, _ in cubes) + 1
    min_y = min(y for _, y, _ in cubes) - 1
    max_y = max(y for _, y, _ in cubes) + 1
    min_z = min(z for _, _, z in cubes) - 1
    max_z = max(z for _, _, z in cubes) + 1

    start = (min_x, min_y, min_z)
    queue = deque([start])
    visited = {start}
    surface = 0

    def in_bounds(pos):
        x, y, z = pos
        return (
            min_x <= x <= max_x
            and min_y <= y <= max_y
            and min_z <= z <= max_z
        )

    while queue:
        x, y, z = queue.popleft()
        for dx, dy, dz in DIRECTIONS:
            neighbor = (x + dx, y + dy, z + dz)
            if neighbor in cubes:
                surface += 1
            elif in_bounds(neighbor) and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return surface


def run_example() -> None:
    example = dedent(
        """\
        2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
        """
    )
    assert part1(example) == 64
    assert part2(example) == 58
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

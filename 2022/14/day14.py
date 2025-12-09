import os
import sys
from textwrap import dedent


def parse(data: str) -> set[tuple[int, int]]:
    rocks = set()
    for line in data.strip().splitlines():
        points = [tuple(map(int, part.strip().split(","))) for part in line.split("->")]
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            if x1 == x2:
                step = 1 if y2 >= y1 else -1
                for y in range(y1, y2 + step, step):
                    rocks.add((x1, y))
            elif y1 == y2:
                step = 1 if x2 >= x1 else -1
                for x in range(x1, x2 + step, step):
                    rocks.add((x, y1))
            else:
                raise ValueError("Segments must be horizontal or vertical")
    return rocks


def drop_sand(blocked: set[tuple[int, int]], max_y: int, floor: int | None) -> tuple[int, int] | None:
    x, y = 500, 0
    while True:
        moved = False
        for dx in (0, -1, 1):
            nx, ny = x + dx, y + 1
            if floor is not None and ny == floor:
                continue
            if (nx, ny) not in blocked:
                x, y = nx, ny
                moved = True
                break
        if not moved:
            blocked.add((x, y))
            return (x, y)
        if floor is None and y > max_y:
            return None


def simulate(data: str, with_floor: bool) -> int:
    blocked = parse(data)
    max_y = max(y for _, y in blocked)
    floor = max_y + 2 if with_floor else None
    count = 0
    while True:
        settled = drop_sand(blocked, max_y, floor)
        if settled is None:
            return count
        count += 1
        if with_floor and settled == (500, 0):
            return count


def part1(data: str) -> int:
    return simulate(data, with_floor=False)


def part2(data: str) -> int:
    return simulate(data, with_floor=True)


def run_example() -> None:
    example = dedent(
        """\
        498,4 -> 498,6 -> 496,6
        503,4 -> 502,4 -> 502,9 -> 494,9
        """
    )
    assert part1(example) == 24
    assert part2(example) == 93
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

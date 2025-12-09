import os
import sys
from textwrap import dedent


def parse(data: str) -> list[tuple[str, int]]:
    steps = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        direction, count = line.split()
        steps.append((direction, int(count)))
    return steps


def sign(x: int) -> int:
    if x == 0:
        return 0
    return 1 if x > 0 else -1


def simulate(data: str, rope_length: int) -> int:
    knots = [[0, 0] for _ in range(rope_length)]
    visited = {tuple(knots[-1])}
    moves = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
    }

    for direction, count in parse(data):
        dx, dy = moves[direction]
        for _ in range(count):
            knots[0][0] += dx
            knots[0][1] += dy
            for i in range(1, rope_length):
                hx, hy = knots[i - 1]
                tx, ty = knots[i]
                if max(abs(hx - tx), abs(hy - ty)) <= 1:
                    continue
                knots[i][0] += sign(hx - tx)
                knots[i][1] += sign(hy - ty)
            visited.add(tuple(knots[-1]))
    return len(visited)


def part1(data: str) -> int:
    return simulate(data, rope_length=2)


def part2(data: str) -> int:
    return simulate(data, rope_length=10)


def run_example() -> None:
    example = dedent(
        """\
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
        """
    )
    assert part1(example) == 13

    example2 = dedent(
        """\
        R 5
        U 8
        L 8
        D 3
        R 17
        D 10
        L 25
        U 20
        """
    )
    assert part2(example2) == 36
    print("✓ Examples passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

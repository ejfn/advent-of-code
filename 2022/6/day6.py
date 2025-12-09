import os
import sys
from textwrap import dedent


def find_marker(stream: str, size: int) -> int:
    for i in range(size, len(stream) + 1):
        window = stream[i - size : i]
        if len(set(window)) == size:
            return i
    raise ValueError("Marker not found")


def part1(data: str) -> int:
    return find_marker(data.strip(), 4)


def part2(data: str) -> int:
    return find_marker(data.strip(), 14)


def run_example() -> None:
    example = dedent(
        """\
        mjqjpqmgbljsphdztnvjfqwrcgsmlb
        """
    ).strip()
    assert part1(example) == 7
    assert part2(example) == 19
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

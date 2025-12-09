import os
import sys
from textwrap import dedent


def mix(values, rounds=1, key=1):
    items = [(value * key, idx) for idx, value in enumerate(values)]
    order = list(items)
    length = len(items)

    for _ in range(rounds):
        for item in order:
            idx = items.index(item)
            items.pop(idx)
            value = item[0]
            new_idx = (idx + value) % (length - 1)
            items.insert(new_idx, item)

    zero_index = next(i for i, (value, _) in enumerate(items) if value == 0)
    total = 0
    for offset in (1000, 2000, 3000):
        total += items[(zero_index + offset) % length][0]
    return total


def part1(data: str) -> int:
    values = [int(line) for line in data.strip().splitlines()]
    return mix(values, rounds=1, key=1)


def part2(data: str) -> int:
    values = [int(line) for line in data.strip().splitlines()]
    return mix(values, rounds=10, key=811589153)


def run_example() -> None:
    example = dedent(
        """\
        1
        2
        -3
        3
        -2
        0
        4
        """
    )
    assert part1(example) == 3
    assert part2(example) == 1623178306
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

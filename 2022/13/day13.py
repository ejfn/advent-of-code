import ast
import functools
import os
import sys
from textwrap import dedent
from typing import Any, List


def compare(left: Any, right: Any) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return (left > right) - (left < right)
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for l_item, r_item in zip(left, right):
        cmp = compare(l_item, r_item)
        if cmp != 0:
            return cmp
    return (len(left) > len(right)) - (len(left) < len(right))


def parse_pairs(data: str) -> List[tuple[Any, Any]]:
    pairs = []
    for block in data.strip().split("\n\n"):
        left, right = block.splitlines()
        pairs.append((ast.literal_eval(left), ast.literal_eval(right)))
    return pairs


def part1(data: str) -> int:
    total = 0
    for idx, (left, right) in enumerate(parse_pairs(data), start=1):
        if compare(left, right) == -1:
            total += idx
    return total


def part2(data: str) -> int:
    packets = []
    for left, right in parse_pairs(data):
        packets.extend([left, right])
    dividers = [[[2]], [[6]]]
    packets.extend(dividers)
    packets.sort(key=functools.cmp_to_key(compare))
    pos1 = packets.index(dividers[0]) + 1
    pos2 = packets.index(dividers[1]) + 1
    return pos1 * pos2


def run_example() -> None:
    example = dedent(
        """\
        [1,1,3,1,1]
        [1,1,5,1,1]

        [[1],[2,3,4]]
        [[1],4]

        [9]
        [[8,7,6]]

        [[4,4],4,4]
        [[4,4],4,4,4]

        [7,7,7,7]
        [7,7,7]

        []
        [3]

        [[[]]]
        [[]]

        [1,[2,[3,[4,[5,6,7]]]],8,9]
        [1,[2,[3,[4,[5,6,0]]]],8,9]
        """
    )
    assert part1(example) == 13
    assert part2(example) == 140
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

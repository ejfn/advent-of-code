import os
import sys


def parse_calorie_groups(raw: str) -> list[int]:
    groups = []
    current = 0
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            groups.append(current)
            current = 0
        else:
            current += int(line)
    groups.append(current)
    return groups


def part1(data: str) -> int:
    groups = parse_calorie_groups(data)
    return max(groups)


def part2(data: str) -> int:
    groups = sorted(parse_calorie_groups(data), reverse=True)
    return sum(groups[:3])


def run_example() -> None:
    example = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    assert part1(example) == 24000
    assert part2(example) == 45000
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip("\n")
    print(part1(puzzle_input))
    print(part2(puzzle_input))

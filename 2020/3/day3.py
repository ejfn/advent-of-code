import os
import sys
from typing import List, Tuple


def parse(data: str) -> List[str]:
    return [line.strip() for line in data.splitlines() if line.strip()]


def trees_on_slope(grid: List[str], right: int, down: int) -> int:
    width = len(grid[0])
    r = c = trees = 0
    while r < len(grid):
        if grid[r][c % width] == '#':
            trees += 1
        r += down
        c += right
    return trees


def part1(data: str) -> int:
    grid = parse(data)
    return trees_on_slope(grid, 3, 1)


def part2(data: str) -> int:
    grid = parse(data)
    slopes: List[Tuple[int, int]] = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    prod = 1
    for right, down in slopes:
        prod *= trees_on_slope(grid, right, down)
    return prod


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
    print("Example Part 1:", part1(example))  # Expected 7
    print("Example Part 2:", part2(example))  # Expected 336


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

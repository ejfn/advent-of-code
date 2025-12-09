import os
import sys
from textwrap import dedent


def parse(data: str) -> list[list[int]]:
    return [[int(c) for c in line.strip()] for line in data.strip().splitlines() if line.strip()]


def part1(data: str) -> int:
    grid = parse(data)
    rows, cols = len(grid), len(grid[0])
    visible = 0
    for r in range(rows):
        for c in range(cols):
            height = grid[r][c]
            left = all(grid[r][cc] < height for cc in range(0, c))
            right = all(grid[r][cc] < height for cc in range(c + 1, cols))
            up = all(grid[rr][c] < height for rr in range(0, r))
            down = all(grid[rr][c] < height for rr in range(r + 1, rows))
            if left or right or up or down:
                visible += 1
    return visible


def viewing_distance(line, height):
    distance = 0
    for h in line:
        distance += 1
        if h >= height:
            break
    return distance


def part2(data: str) -> int:
    grid = parse(data)
    rows, cols = len(grid), len(grid[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            height = grid[r][c]
            left = viewing_distance(reversed([grid[r][cc] for cc in range(0, c)]), height)
            right = viewing_distance([grid[r][cc] for cc in range(c + 1, cols)], height)
            up = viewing_distance(reversed([grid[rr][c] for rr in range(0, r)]), height)
            down = viewing_distance([grid[rr][c] for rr in range(r + 1, rows)], height)
            best = max(best, left * right * up * down)
    return best


def run_example() -> None:
    example = dedent(
        """\
        30373
        25512
        65332
        33549
        35390
        """
    )
    assert part1(example) == 21
    assert part2(example) == 8
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

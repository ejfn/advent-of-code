import os
import sys
from typing import Callable, List, Tuple

Grid = List[List[str]]
DIRECTIONS: Tuple[Tuple[int, int], ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def parse(data: str) -> Grid:
    return [list(line.strip()) for line in data.splitlines() if line.strip()]


def count_adjacent(grid: Grid, r: int, c: int) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '#':
            count += 1
    return count


def count_visible(grid: Grid, r: int, c: int) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        while 0 <= nr < rows and 0 <= nc < cols:
            seat = grid[nr][nc]
            if seat == '#':
                count += 1
                break
            if seat == 'L':
                break
            nr += dr
            nc += dc
    return count


def simulate(grid: Grid, tolerance: int, visible_counter: Callable[[Grid, int, int], int]) -> int:
    rows, cols = len(grid), len(grid[0])
    changed = True
    current = [row[:] for row in grid]
    while changed:
        changed = False
        new_grid = [row[:] for row in current]
        for r in range(rows):
            for c in range(cols):
                seat = current[r][c]
                if seat == '.':
                    continue
                occupied = visible_counter(current, r, c)
                if seat == 'L' and occupied == 0:
                    new_grid[r][c] = '#'
                    changed = True
                elif seat == '#' and occupied >= tolerance:
                    new_grid[r][c] = 'L'
                    changed = True
        current = new_grid
    return sum(row.count('#') for row in current)


def part1(data: str) -> int:
    grid = parse(data)
    return simulate(grid, 4, count_adjacent)


def part2(data: str) -> int:
    grid = parse(data)
    return simulate(grid, 5, count_visible)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    print("Example Part 1:", part1(example))  # Expected 37
    print("Example Part 2:", part2(example))  # Expected 26


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

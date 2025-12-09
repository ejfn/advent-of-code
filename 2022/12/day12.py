import os
import sys
from collections import deque
from textwrap import dedent
from typing import Tuple


def parse(data: str):
    grid = []
    start = end = None
    for r, line in enumerate(data.strip().splitlines()):
        row = []
        for c, ch in enumerate(line.strip()):
            if ch == "S":
                start = (r, c)
                row.append(0)
            elif ch == "E":
                end = (r, c)
                row.append(25)
            else:
                row.append(ord(ch) - ord("a"))
        grid.append(row)
    return grid, start, end


def bfs(grid, start, is_goal, can_move):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])
    seen = {start}
    while queue:
        r, c, dist = queue.popleft()
        if is_goal(r, c):
            return dist
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc) not in seen and can_move((r, c), (nr, nc)):
                    seen.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return None


def part1(data: str) -> int:
    grid, start, end = parse(data)

    def can_move(current, nxt):
        r1, c1 = current
        r2, c2 = nxt
        return grid[r2][c2] <= grid[r1][c1] + 1

    return bfs(grid, start, lambda r, c: (r, c) == end, can_move)


def part2(data: str) -> int:
    grid, start, end = parse(data)

    def can_move(current, nxt):
        r1, c1 = current
        r2, c2 = nxt
        return grid[r2][c2] >= grid[r1][c1] - 1

    return bfs(grid, end, lambda r, c: grid[r][c] == 0, can_move)


def run_example() -> None:
    example = dedent(
        """\
        Sabqponm
        abcryxxl
        accszExk
        acctuvwj
        abdefghi
        """
    )
    assert part1(example) == 31
    assert part2(example) == 29
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

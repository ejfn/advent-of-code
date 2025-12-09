import os
import sys
from collections import deque
from math import lcm
from typing import Deque, Iterable, List, Sequence, Set, Tuple

Grid = List[str]
Position = Tuple[int, int]
Blizzard = Tuple[int, int, int, int]

DIRECTION_MAP = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def parse(data: str) -> Tuple[Grid, Position, Position, List[Blizzard]]:
    grid = data.splitlines()
    height = len(grid)
    width = len(grid[0])
    start_col = grid[0].index('.')
    end_col = grid[-1].index('.')
    start = (0, start_col)
    goal = (height - 1, end_col)

    blizzards: List[Blizzard] = []
    for r in range(height):
        for c in range(width):
            ch = grid[r][c]
            if ch in DIRECTION_MAP:
                dr, dc = DIRECTION_MAP[ch]
                blizzards.append((r, c, dr, dc))
    return grid, start, goal, blizzards


def build_states(blizzards: Sequence[Blizzard], height: int, width: int) -> List[Set[Position]]:
    inner_h = height - 2
    inner_w = width - 2
    cycle = lcm(inner_h, inner_w)
    states: List[Set[Position]] = []

    for minute in range(cycle):
        occupied: Set[Position] = set()
        for r, c, dr, dc in blizzards:
            nr = ((r - 1 + dr * minute) % inner_h) + 1
            nc = ((c - 1 + dc * minute) % inner_w) + 1
            occupied.add((nr, nc))
        states.append(occupied)
    return states


def bfs(grid: Grid, start: Position, goal: Position, blizzard_states: Sequence[Set[Position]], start_time: int) -> int:
    height = len(grid)
    width = len(grid[0])
    cycle = len(blizzard_states)
    queue: Deque[Tuple[int, int, int]] = deque([(start[0], start[1], start_time)])
    seen: Set[Tuple[int, int, int]] = {(start[0], start[1], start_time % cycle)}

    while queue:
        r, c, minute = queue.popleft()
        next_minute = minute + 1
        blocked = blizzard_states[next_minute % cycle]
        for dr, dc in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) == goal:
                return next_minute
            if not (0 <= nr < height and 0 <= nc < width):
                continue
            if grid[nr][nc] == '#':
                continue
            if (nr, nc) in blocked:
                continue
            state = (nr, nc, next_minute % cycle)
            if state in seen:
                continue
            seen.add(state)
            queue.append((nr, nc, next_minute))
    raise RuntimeError("No path found")


def part1(data: str) -> int:
    grid, start, goal, blizzards = parse(data.strip())
    states = build_states(blizzards, len(grid), len(grid[0]))
    return bfs(grid, start, goal, states, 0)


def part2(data: str) -> int:
    grid, start, goal, blizzards = parse(data.strip())
    states = build_states(blizzards, len(grid), len(grid[0]))
    first = bfs(grid, start, goal, states, 0)
    second = bfs(grid, goal, start, states, first)
    third = bfs(grid, start, goal, states, second)
    return third


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """#.######\n#>>.<^<#\n#.<..<<#\n#>v.><>#\n#<^v^^>#\n######.#"""
    print("Example Part 1:", part1(example))  # Expected 18
    print("Example Part 2:", part2(example))  # Expected 54


if __name__ == "__main__":
    data = read_input()
    print(part1(data))
    print(part2(data))

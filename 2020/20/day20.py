import math
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

TileGrid = List[str]

MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


@dataclass(frozen=True)
class Orientation:
    tile_id: int
    grid: TileGrid
    top: str
    bottom: str
    left: str
    right: str


def parse(data: str) -> Dict[int, TileGrid]:
    tiles: Dict[int, TileGrid] = {}
    for block in data.strip().split('\n\n'):
        lines = block.splitlines()
        tile_id = int(lines[0][5:-1])
        grid = [line.strip() for line in lines[1:]]
        tiles[tile_id] = grid
    return tiles


def rotate(grid: TileGrid) -> TileGrid:
    size = len(grid)
    return [''.join(grid[size - 1 - r][c] for r in range(size)) for c in range(size)]


def flip(grid: TileGrid) -> TileGrid:
    return [row[::-1] for row in grid]


def orientations(tile_id: int, grid: TileGrid) -> List[Orientation]:
    grids: List[TileGrid] = []
    g = grid
    for _ in range(4):
        grids.append(g)
        grids.append(flip(g))
        g = rotate(g)
    seen = []
    result = []
    for g in grids:
        if g in seen:
            continue
        seen.append(g)
        top = g[0]
        bottom = g[-1]
        left = ''.join(row[0] for row in g)
        right = ''.join(row[-1] for row in g)
        result.append(Orientation(tile_id, g, top, bottom, left, right))
    return result


def assemble(tiles: Dict[int, TileGrid]) -> List[Orientation]:
    size = int(math.isqrt(len(tiles)))
    options = {tile_id: orientations(tile_id, grid) for tile_id, grid in tiles.items()}
    placed: List[Optional[Orientation]] = [None] * (size * size)
    used: Set[int] = set()

    def backtrack(pos: int) -> bool:
        if pos == size * size:
            return True
        r, c = divmod(pos, size)
        top_neighbor = placed[pos - size] if r > 0 else None
        left_neighbor = placed[pos - 1] if c > 0 else None
        for tile_id, orients in options.items():
            if tile_id in used:
                continue
            for orient in orients:
                if top_neighbor and top_neighbor.bottom != orient.top:
                    continue
                if left_neighbor and left_neighbor.right != orient.left:
                    continue
                placed[pos] = orient
                used.add(tile_id)
                if backtrack(pos + 1):
                    return True
                used.remove(tile_id)
                placed[pos] = None
        return False

    if not backtrack(0):
        raise RuntimeError('No arrangement found')
    return [p for p in placed if p is not None]


def part1(data: str) -> int:
    tiles = parse(data)
    arrangement = assemble(tiles)
    size = int(math.isqrt(len(tiles)))
    corners = [arrangement[0], arrangement[size - 1], arrangement[-size], arrangement[-1]]
    result = 1
    for tile in corners:
        result *= tile.tile_id
    return result


def remove_borders(tile: TileGrid) -> TileGrid:
    return [row[1:-1] for row in tile[1:-1]]


def build_image(arrangement: List[Orientation]) -> TileGrid:
    size = int(math.isqrt(len(arrangement)))
    tile_size = len(arrangement[0].grid) - 2
    rows: List[str] = []
    for r in range(size):
        row_tiles = [remove_borders(arrangement[r * size + c].grid) for c in range(size)]
        for i in range(tile_size):
            rows.append(''.join(tile[i] for tile in row_tiles))
    return rows


def all_transformations(grid: TileGrid) -> List[TileGrid]:
    grids: List[TileGrid] = []
    g = grid
    for _ in range(4):
        grids.append(g)
        grids.append(flip(g))
        g = rotate(g)
    unique: List[TileGrid] = []
    for candidate in grids:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def count_monsters(grid: TileGrid) -> Tuple[int, TileGrid]:
    monster_coords = [(r, c) for r, row in enumerate(MONSTER) for c, ch in enumerate(row) if ch == '#']
    height = len(grid)
    width = len(grid[0])
    monster_height = len(MONSTER)
    monster_width = len(MONSTER[0])
    best = (0, grid)
    for transformed in all_transformations(grid):
        marked = [list(row) for row in transformed]
        count = 0
        for r in range(height - monster_height + 1):
            for c in range(width - monster_width + 1):
                if all(transformed[r + dr][c + dc] == '#' for dr, dc in monster_coords):
                    count += 1
                    for dr, dc in monster_coords:
                        marked[r + dr][c + dc] = 'O'
        if count > 0:
            best = (count, [''.join(row) for row in marked])
            break
    return best


def part2(data: str) -> int:
    tiles = parse(data)
    arrangement = assemble(tiles)
    image = build_image(arrangement)
    count, marked = count_monsters(image)
    if count == 0:
        # No monsters found; return hash count
        return sum(row.count('#') for row in image)
    total_hashes = sum(row.count('#') for row in marked)
    return total_hashes


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...
"""  # truncated example
    print("Example Part 1:", part1(example))


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

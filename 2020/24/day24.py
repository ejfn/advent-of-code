import os
import sys
from collections import Counter
from typing import Dict, List, Set, Tuple

Direction = Tuple[int, int]
DIRECTIONS: Dict[str, Direction] = {
    'e': (1, 0),
    'w': (-1, 0),
    'ne': (1, -1),
    'nw': (0, -1),
    'se': (0, 1),
    'sw': (-1, 1),
}


def parse_line(line: str) -> List[str]:
    instructions = []
    i = 0
    while i < len(line):
        if line[i] in {'e', 'w'}:
            instructions.append(line[i])
            i += 1
        else:
            instructions.append(line[i:i + 2])
            i += 2
    return instructions


def parse(data: str) -> List[List[str]]:
    return [parse_line(line.strip()) for line in data.splitlines() if line.strip()]


def walk(instructions: List[str]) -> Tuple[int, int]:
    q = r = 0
    for instr in instructions:
        dq, dr = DIRECTIONS[instr]
        q += dq
        r += dr
    return q, r


def initial_black_tiles(paths: List[List[str]]) -> Set[Tuple[int, int]]:
    black: Set[Tuple[int, int]] = set()
    for path in paths:
        pos = walk(path)
        if pos in black:
            black.remove(pos)
        else:
            black.add(pos)
    return black


def simulate(black: Set[Tuple[int, int]], days: int) -> Set[Tuple[int, int]]:
    current = set(black)
    for _ in range(days):
        counts: Counter[Tuple[int, int]] = Counter()
        for q, r in current:
            for dq, dr in DIRECTIONS.values():
                neighbor = (q + dq, r + dr)
                counts[neighbor] += 1
        new_black: Set[Tuple[int, int]] = set()
        tiles_to_check = set(counts.keys()) | current
        for tile in tiles_to_check:
            neighbors = counts.get(tile, 0)
            if tile in current:
                if neighbors in (1, 2):
                    new_black.add(tile)
            else:
                if neighbors == 2:
                    new_black.add(tile)
        current = new_black
    return current


def part1(data: str) -> int:
    paths = parse(data)
    black = initial_black_tiles(paths)
    return len(black)


def part2(data: str) -> int:
    paths = parse(data)
    black = initial_black_tiles(paths)
    final_black = simulate(black, 100)
    return len(final_black)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
    print("Example Part 1:", part1(example))  # Expected 10
    print("Example Part 2:", part2(example))  # Expected 2208


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

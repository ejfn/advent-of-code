import os
import sys
from collections import deque
from functools import lru_cache


def build_paths(layout):
    """Precompute all shortest move strings (ending in 'A') between every pair."""
    positions = {key: (r, c) for key, (r, c) in layout.items()}
    coord_set = set(positions.values())
    keys = list(layout.keys())
    dirs = [(-1, 0, "^"), (1, 0, "v"), (0, -1, "<"), (0, 1, ">")]

    def shortest_paths(src_key, dst_key):
        src = positions[src_key]
        dst = positions[dst_key]

        # BFS for distances
        dist = {src: 0}
        q = deque([src])
        while q:
            r, c = q.popleft()
            if (r, c) == dst:
                break
            for dr, dc, _ in dirs:
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_set and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))

        target_dist = dist[dst]
        paths = []

        # DFS following only edges that advance along the shortest-path DAG.
        def dfs(pos, path):
            if pos == dst:
                paths.append(path)
                return
            r, c = pos
            for dr, dc, ch in dirs:
                nr, nc = r + dr, c + dc
                if (nr, nc) in dist and dist[(nr, nc)] == dist[(r, c)] + 1:
                    dfs((nr, nc), path + ch)

        dfs(src, "")
        return [p + "A" for p in paths]

    moves = {k: {} for k in keys}
    for a in keys:
        for b in keys:
            moves[a][b] = shortest_paths(a, b)
    return moves


# Define keypad layouts
NUMERIC_LAYOUT = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

DIR_LAYOUT = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

NUMERIC_MOVES = build_paths(NUMERIC_LAYOUT)
DIR_MOVES = build_paths(DIR_LAYOUT)


@lru_cache(maxsize=None)
def type_cost(seq, depth):
    """
    Minimal button presses with `depth` directional keypads above the one
    receiving `seq`. depth=0 means we are pressing the buttons directly.
    """
    if depth == 0:
        return len(seq)

    total = 0
    prev = "A"
    for ch in seq:
        best = min(type_cost(path, depth - 1) for path in DIR_MOVES[prev][ch])
        total += best
        prev = ch
    return total


def code_cost(code, depth):
    """Cost to enter a full code on the numeric keypad."""
    total = 0
    prev = "A"
    for ch in code:
        best = min(type_cost(path, depth) for path in NUMERIC_MOVES[prev][ch])
        total += best
        prev = ch
    return total


def parse_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]


def solve(codes, robots):
    """Sum complexities (cost * numeric part) given robot depth."""
    total = 0
    for code in codes:
        cost = code_cost(code, robots)
        numeric_value = int(code[:-1])
        total += cost * numeric_value
    return total


def part1():
    input_file = os.path.join(sys.path[0], "input.txt")
    codes = parse_input(input_file)
    return solve(codes, robots=2)


def part2():
    input_file = os.path.join(sys.path[0], "input.txt")
    codes = parse_input(input_file)
    return solve(codes, robots=25)


def run_example():
    """Run the sample from the puzzle description."""
    example = ["029A", "980A", "179A", "456A", "379A"]
    print("Example with 2 robots (part 1 rules):")
    print(solve(example, robots=2))
    print("Example with 25 robots (part 2 rules):")
    print(solve(example, robots=25))


if __name__ == "__main__":
    print("=== Example ===")
    run_example()

    input_file = os.path.join(sys.path[0], "input.txt")
    if os.path.exists(input_file):
        print("\n=== Part 1 ===")
        print(part1())

        print("\n=== Part 2 ===")
        print(part2())
    else:
        print("\nNo input.txt found in this directory. Add your puzzle input to run part 1 and part 2.")

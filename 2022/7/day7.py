import os
import sys
from collections import defaultdict
from textwrap import dedent


def compute_sizes(data: str) -> dict[tuple[str, ...], int]:
    sizes = defaultdict(int)
    stack: list[str] = []

    for line in data.strip().splitlines():
        line = line.strip()
        if line.startswith("$ cd"):
            target = line.split()[-1]
            if target == "/":
                stack = []
            elif target == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(target)
        elif line.startswith("$ ls") or line.startswith("dir "):
            continue
        else:
            size = int(line.split()[0])
            for i in range(len(stack) + 1):
                path = tuple(stack[:i])
                sizes[path] += size
    return sizes


def part1(data: str) -> int:
    sizes = compute_sizes(data)
    return sum(size for size in sizes.values() if size <= 100_000)


def part2(data: str) -> int:
    sizes = compute_sizes(data)
    total_used = sizes[tuple()]
    total_disk = 70_000_000
    required_free = 30_000_000
    current_free = total_disk - total_used
    need_to_free = max(0, required_free - current_free)
    if need_to_free == 0:
        return 0
    candidates = [size for size in sizes.values() if size >= need_to_free]
    return min(candidates)


def run_example() -> None:
    example = dedent(
        """\
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
        """
    )
    assert part1(example) == 95437
    assert part2(example) == 24933642
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

import os
import sys
from copy import deepcopy
from textwrap import dedent


def parse(data: str):
    drawing, moves = data.split("\n\n")
    drawing_lines = drawing.splitlines()
    stack_ids = drawing_lines[-1].split()
    stack_count = int(stack_ids[-1])
    stacks = [[] for _ in range(stack_count)]

    for line in reversed(drawing_lines[:-1]):
        for idx in range(stack_count):
            col = 1 + idx * 4
            if col < len(line):
                char = line[col]
                if char.strip():
                    stacks[idx].append(char)

    instructions = []
    for line in moves.strip().splitlines():
        parts = line.split()
        qty = int(parts[1])
        src = int(parts[3]) - 1
        dst = int(parts[5]) - 1
        instructions.append((qty, src, dst))
    return stacks, instructions


def run(stacks, instructions, bulk_move=False):
    stacks = deepcopy(stacks)
    for qty, src, dst in instructions:
        if bulk_move:
            block = stacks[src][-qty:]
            stacks[src] = stacks[src][:-qty]
            stacks[dst].extend(block)
        else:
            for _ in range(qty):
                stacks[dst].append(stacks[src].pop())
    return "".join(stack[-1] for stack in stacks)


def part1(data: str) -> str:
    stacks, instructions = parse(data)
    return run(stacks, instructions, bulk_move=False)


def part2(data: str) -> str:
    stacks, instructions = parse(data)
    return run(stacks, instructions, bulk_move=True)


def run_example() -> None:
    example = dedent(
        """\
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        """
    )
    assert part1(example) == "CMZ"
    assert part2(example) == "MCD"
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

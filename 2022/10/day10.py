import os
import sys
from textwrap import dedent
from typing import Iterable, List


LETTER_MAP = {
    (
        ".##.",
        "#..#",
        "#..#",
        "####",
        "#..#",
        "#..#",
    ): "A",
    (
        "###.",
        "#..#",
        "###.",
        "#..#",
        "#..#",
        "###.",
    ): "B",
    (
        ".##.",
        "#..#",
        "#...",
        "#...",
        "#..#",
        ".##.",
    ): "C",
    (
        "###.",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "###.",
    ): "D",
    (
        "####",
        "#...",
        "###.",
        "#...",
        "#...",
        "####",
    ): "E",
    (
        "####",
        "#...",
        "###.",
        "#...",
        "#...",
        "#...",
    ): "F",
    (
        ".##.",
        "#..#",
        "#...",
        "#.##",
        "#..#",
        ".###",
    ): "G",
    (
        "#..#",
        "#..#",
        "####",
        "#..#",
        "#..#",
        "#..#",
    ): "H",
    (
        ".##.",
        "..#.",
        "..#.",
        "..#.",
        "..#.",
        ".##.",
    ): "I",
    (
        "..##",
        "...#",
        "...#",
        "...#",
        "#..#",
        ".##.",
    ): "J",
    (
        "#..#",
        "#.#.",
        "##..",
        "#.#.",
        "#.#.",
        "#..#",
    ): "K",
    (
        "#...",
        "#...",
        "#...",
        "#...",
        "#...",
        "####",
    ): "L",
    (
        ".##.",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        ".##.",
    ): "O",
    (
        "###.",
        "#..#",
        "#..#",
        "###.",
        "#...",
        "#...",
    ): "P",
    (
        "###.",
        "#..#",
        "#..#",
        "###.",
        "#.#.",
        "#..#",
    ): "R",
    (
        ".###",
        "#...",
        "#...",
        ".##.",
        "...#",
        "###.",
    ): "S",
    (
        "####",
        "..#.",
        "..#.",
        "..#.",
        "..#.",
        "..#.",
    ): "T",
    (
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        ".##.",
    ): "U",
    (
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        ".##.",
        ".##.",
    ): "V",
    (
        "#..#",
        "#..#",
        "#..#",
        "#..#",
        "####",
        "#..#",
    ): "W",
    (
        "#..#",
        ".##.",
        "..#.",
        ".##.",
        "#..#",
        "#..#",
    ): "X",
    (
        "#..#",
        "#..#",
        ".##.",
        "..#.",
        "..#.",
        "..#.",
    ): "Y",
    (
        "####",
        "...#",
        "..#.",
        ".#..",
        "#...",
        "####",
    ): "Z",
}


def parse(data: str) -> list[tuple[str, int]]:
    instructions = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if parts[0] == "noop":
            instructions.append(("noop", 0))
        else:
            instructions.append(("addx", int(parts[1])))
    return instructions


def run_program(data: str):
    x = 1
    cycle = 0
    for op, value in parse(data):
        if op == "noop":
            cycle += 1
            yield cycle, x
        else:
            for _ in range(2):
                cycle += 1
                yield cycle, x
            x += value


def part1(data: str) -> int:
    interesting = {20, 60, 100, 140, 180, 220}
    total = 0
    for cycle, x in run_program(data):
        if cycle in interesting:
            total += cycle * x
    return total


def draw_display(data: str) -> list[str]:
    pixels = []
    for cycle, x in run_program(data):
        pos = (cycle - 1) % 40
        if abs(pos - x) <= 1:
            pixels.append("#")
        else:
            pixels.append(".")
    lines = ["".join(pixels[i : i + 40]) for i in range(0, len(pixels), 40)]
    return lines[:6]


def decode_display(lines: List[str]) -> str:
    width = len(lines[0])
    letters = []
    for start in range(0, width, 5):
        pattern = tuple(line[start : start + 4] for line in lines)
        letters.append(LETTER_MAP.get(pattern, "?"))
    return "".join(letters)


def part2(data: str) -> str:
    lines = draw_display(data)
    decoded = decode_display(lines)
    if "?" in decoded:
        return "\n".join(lines)
    return decoded


def run_example() -> None:
    example = dedent(
        """\
        addx 15
        addx -11
        addx 6
        addx -3
        addx 5
        addx -1
        addx -8
        addx 13
        addx 4
        noop
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx 5
        addx -1
        addx -35
        addx 1
        addx 24
        addx -19
        addx 1
        addx 16
        addx -11
        noop
        noop
        addx 21
        addx -15
        noop
        noop
        addx -3
        addx 9
        addx 1
        addx -3
        addx 8
        addx 1
        addx 5
        noop
        noop
        noop
        noop
        noop
        addx -36
        noop
        addx 1
        addx 7
        noop
        noop
        noop
        addx 2
        addx 6
        noop
        noop
        noop
        noop
        noop
        addx 1
        noop
        noop
        addx 7
        addx 1
        noop
        addx -13
        addx 13
        addx 7
        noop
        addx 1
        addx -33
        noop
        noop
        noop
        addx 2
        noop
        noop
        noop
        addx 8
        noop
        addx -1
        addx 2
        addx 1
        noop
        addx 17
        addx -9
        addx 1
        addx 1
        addx -3
        addx 11
        noop
        noop
        addx 1
        noop
        addx 1
        noop
        noop
        addx -13
        addx -19
        addx 1
        addx 3
        addx 26
        addx -30
        addx 12
        addx -1
        addx 3
        addx 1
        noop
        noop
        noop
        addx -9
        addx 18
        addx 1
        addx 2
        noop
        noop
        addx 9
        noop
        noop
        noop
        addx -1
        addx 2
        addx -37
        addx 1
        addx 3
        noop
        addx 15
        addx -21
        addx 22
        addx -6
        addx 1
        noop
        addx 2
        addx 1
        noop
        addx -10
        noop
        noop
        addx 20
        addx 1
        addx 2
        addx 2
        addx -6
        addx -11
        noop
        noop
        noop
        """
    )
    assert part1(example) == 13140
    expected = dedent(
        """\
        ##..##..##..##..##..##..##..##..##..##..
        ###...###...###...###...###...###...###.
        ####....####....####....####....####....
        #####.....#####.....#####.....#####.....
        ######......######......######......####
        #######.......#######.......#######.....
        """
    ).strip()
    assert part2(example) == expected
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

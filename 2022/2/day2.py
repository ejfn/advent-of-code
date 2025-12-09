import os
import sys


OPPONENT = {"A": 0, "B": 1, "C": 2}
YOU = {"X": 0, "Y": 1, "Z": 2}


def parse(data: str) -> list[tuple[int, int]]:
    rounds = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        opp, me = line.split()
        rounds.append((OPPONENT[opp], YOU[me]))
    return rounds


def score_round(opp: int, me: int) -> int:
    outcome = (me - opp) % 3
    if outcome == 0:
        bonus = 3
    elif outcome == 1:
        bonus = 6
    else:
        bonus = 0
    return me + 1 + bonus


def part1(data: str) -> int:
    return sum(score_round(opp, me) for opp, me in parse(data))


def part2(data: str) -> int:
    total = 0
    for opp, result in parse(data):
        # result: 0 lose, 1 draw, 2 win
        if result == 0:
            me = (opp - 1) % 3
            bonus = 0
        elif result == 1:
            me = opp
            bonus = 3
        else:
            me = (opp + 1) % 3
            bonus = 6
        total += me + 1 + bonus
    return total


def run_example() -> None:
    example = """\
A Y
B X
C Z
"""
    assert part1(example) == 15
    assert part2(example) == 12
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

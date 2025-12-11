import os
import sys
from itertools import cycle


def load_input():
    """Return the list of integer frequency changes from input.txt."""
    input_path = os.path.join(sys.path[0], "input.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]


def part1(changes):
    return sum(changes)


def part2(changes):
    seen = {0}
    current = 0
    for delta in cycle(changes):
        current += delta
        if current in seen:
            return current
        seen.add(current)


def run_example():
    sample = [+1, -2, +3, +1]
    assert part1(sample) == 3
    assert part2(sample) == 2


if __name__ == "__main__":
    run_example()
    data = load_input()
    print(part1(data))
    print(part2(data))

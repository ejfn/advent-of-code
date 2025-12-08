import os
import sys
from functools import lru_cache


def parse_input(filename):
    """Parse the available towel patterns and target designs."""
    with open(filename, "r") as f:
        raw = f.read().strip()

    pattern_block, design_block = raw.split("\n\n", 1)
    patterns = [p.strip() for p in pattern_block.split(",") if p.strip()]
    designs = [line.strip() for line in design_block.splitlines() if line.strip()]
    return patterns, designs


def build_pattern_index(patterns):
    """Group patterns by starting character to cut down on prefix checks."""
    by_first = {}
    for pattern in patterns:
        by_first.setdefault(pattern[0], []).append(pattern)
    return by_first


def count_arrangements(design, patterns_by_first):
    """Count the number of ways to build a design using the patterns."""
    @lru_cache(maxsize=None)
    def ways(idx):
        if idx == len(design):
            return 1

        total = 0
        first_char = design[idx]
        for pattern in patterns_by_first.get(first_char, []):
            if design.startswith(pattern, idx):
                total += ways(idx + len(pattern))
        return total

    return ways(0)


def part1():
    """Count how many designs are possible with the given patterns."""
    input_file = os.path.join(sys.path[0], "input.txt")
    patterns, designs = parse_input(input_file)
    patterns_by_first = build_pattern_index(patterns)

    possible = 0
    for design in designs:
        if count_arrangements(design, patterns_by_first) > 0:
            possible += 1
    return possible


def part2():
    """Sum the total number of arrangements across all designs."""
    input_file = os.path.join(sys.path[0], "input.txt")
    patterns, designs = parse_input(input_file)
    patterns_by_first = build_pattern_index(patterns)

    total_arrangements = 0
    for design in designs:
        total_arrangements += count_arrangements(design, patterns_by_first)
    return total_arrangements


def run_example():
    """Demonstrate the solution on a small, self-contained example."""
    example = """r, wr, b, g, bw, bwr, rb, gbw

bwrb
gbw
rbwr
bg
bw"""

    tmp_path = "/tmp/aoc2024_day19_example.txt"
    with open(tmp_path, "w") as f:
        f.write(example)

    patterns, designs = parse_input(tmp_path)
    patterns_by_first = build_pattern_index(patterns)

    print("Patterns:", patterns)
    for design in designs:
        count = count_arrangements(design, patterns_by_first)
        print(f"{design}: {count} ways")

    possible = sum(1 for d in designs if count_arrangements(d, patterns_by_first) > 0)
    total = sum(count_arrangements(d, patterns_by_first) for d in designs)
    print(f"\nPossible designs: {possible}")
    print(f"Total arrangements across designs: {total}")


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

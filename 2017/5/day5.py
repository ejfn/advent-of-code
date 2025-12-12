import os
import sys


def part1(jumps_orig):
    """Count steps to exit, incrementing offset each jump."""
    jumps = list(jumps_orig)
    pos = 0
    steps = 0
    n = len(jumps)
    while 0 <= pos < n:
        offset = jumps[pos]
        jumps[pos] += 1
        pos += offset
        steps += 1
    return steps


def part2(jumps_orig):
    """Count steps where offset >= 3 decreases, otherwise increases."""
    jumps = list(jumps_orig)
    pos = 0
    steps = 0
    n = len(jumps)
    while 0 <= pos < n:
        offset = jumps[pos]
        if offset >= 3:
            jumps[pos] -= 1
        else:
            jumps[pos] += 1
        pos += offset
        steps += 1
    return steps


def run_example():
    # Part 1 example
    example = [0, 3, 0, 1, -3]
    assert part1(example) == 5
    print("Part 1 example passed!")
    
    # Part 2 example
    assert part2(example) == 10
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        jumps = [int(line.strip()) for line in f if line.strip()]
    
    print(f"Part 1: {part1(jumps)}")
    print(f"Part 2: {part2(jumps)}")

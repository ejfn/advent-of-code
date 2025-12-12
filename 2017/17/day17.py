import os
import sys


def part1(steps):
    """Value after 2017 in the circular buffer."""
    buffer = [0]
    pos = 0
    
    for i in range(1, 2018):
        pos = (pos + steps) % len(buffer)
        buffer.insert(pos + 1, i)
        pos = pos + 1
    
    return buffer[(pos + 1) % len(buffer)]


def part2(steps):
    """Value after 0 after 50 million insertions.
    
    0 is always at position 0. We only need to track when something
    is inserted at position 1 (right after 0).
    """
    pos = 0
    after_zero = None
    
    for i in range(1, 50_000_001):
        pos = (pos + steps) % i
        if pos == 0:
            after_zero = i
        pos = pos + 1
    
    return after_zero


def run_example():
    assert part1(3) == 638
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        steps = int(f.read().strip())
    
    print(f"Part 1: {part1(steps)}")
    print(f"Part 2: {part2(steps)}")

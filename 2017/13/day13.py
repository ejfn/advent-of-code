import os
import sys


def parse_input(text):
    """Parse input into dict of depth -> range."""
    layers = {}
    for line in text.strip().split('\n'):
        if line.strip():
            parts = line.split(': ')
            depth = int(parts[0])
            range_size = int(parts[1])
            layers[depth] = range_size
    return layers


def scanner_at_top(depth, range_size, delay=0):
    """Check if scanner is at top position when packet arrives."""
    # Scanner moves back and forth: period = 2 * (range - 1)
    # Packet arrives at time = depth + delay
    time = depth + delay
    period = 2 * (range_size - 1)
    return time % period == 0


def part1(layers):
    """Calculate severity of trip starting at time 0."""
    severity = 0
    for depth, range_size in layers.items():
        if scanner_at_top(depth, range_size):
            severity += depth * range_size
    return severity


def part2(layers):
    """Find minimum delay to pass through without getting caught."""
    delay = 0
    while True:
        caught = False
        for depth, range_size in layers.items():
            if scanner_at_top(depth, range_size, delay):
                caught = True
                break
        
        if not caught:
            return delay
        delay += 1


def run_example():
    example = """0: 3
1: 2
4: 4
6: 4"""
    layers = parse_input(example)
    assert part1(layers) == 24
    print("Part 1 example passed!")
    assert part2(layers) == 10
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        layers = parse_input(f.read())
    
    print(f"Part 1: {part1(layers)}")
    print(f"Part 2: {part2(layers)}")

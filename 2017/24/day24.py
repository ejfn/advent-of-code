import os
import sys


def parse_input(text):
    """Parse components into list of (a, b) tuples."""
    components = []
    for line in text.strip().split('\n'):
        if '/' in line:
            a, b = map(int, line.split('/'))
            components.append((a, b))
    return components


def build_bridges(components, port, used, current_strength, current_length):
    """Generate all possible bridges from current state."""
    yield (current_strength, current_length)
    
    for i, (a, b) in enumerate(components):
        if i in used:
            continue
        
        if a == port:
            yield from build_bridges(
                components, b, used | {i},
                current_strength + a + b, current_length + 1
            )
        elif b == port:
            yield from build_bridges(
                components, a, used | {i},
                current_strength + a + b, current_length + 1
            )


def part1(components):
    """Find strongest bridge."""
    return max(strength for strength, length in build_bridges(components, 0, set(), 0, 0))


def part2(components):
    """Find strength of longest bridge (tie-break by strength)."""
    bridges = list(build_bridges(components, 0, set(), 0, 0))
    max_length = max(length for strength, length in bridges)
    return max(strength for strength, length in bridges if length == max_length)


def run_example():
    example = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
    components = parse_input(example)
    assert part1(components) == 31
    print("Part 1 example passed!")
    assert part2(components) == 19
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        components = parse_input(f.read())
    
    print(f"Part 1: {part1(components)}")
    print(f"Part 2: {part2(components)}")

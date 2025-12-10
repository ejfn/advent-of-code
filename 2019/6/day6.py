import os
import sys


def parse_input(lines):
    """Parse orbit relationships. A)B means B orbits A."""
    parent = {}
    for line in lines:
        if line.strip():
            a, b = line.strip().split(')')
            parent[b] = a
    return parent


def count_orbits(parent):
    """Count total direct and indirect orbits."""
    # For each object, count how many objects it directly or indirectly orbits
    # (i.e., count depth from each object to COM)
    total = 0
    cache = {}

    def depth(obj):
        if obj not in parent:
            return 0
        if obj in cache:
            return cache[obj]
        d = 1 + depth(parent[obj])
        cache[obj] = d
        return d

    for obj in parent:
        total += depth(obj)

    return total


def run_example():
    """Test with the example from the problem."""
    example = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
    parent = parse_input(example.strip().split('\n'))
    result = count_orbits(parent)
    print(f"Example result: {result} (expected: 42)")
    return result == 42


def part1():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')
    parent = parse_input(lines)
    return count_orbits(parent)


def part2():
    # Will implement after seeing Part 2
    pass


if __name__ == "__main__":
    print("Testing example...")
    if run_example():
        print("Example passed!")
    else:
        print("Example FAILED!")

    print("\nPart 1:", part1())

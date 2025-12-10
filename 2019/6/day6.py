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


def get_path_to_com(parent, obj):
    """Get list of objects from obj up to COM (excluding obj)."""
    path = []
    current = obj
    while current in parent:
        current = parent[current]
        path.append(current)
    return path


def min_transfers(parent, start, end):
    """Find minimum orbital transfers from start's orbit to end's orbit."""
    # Get paths from start and end to COM
    path_start = get_path_to_com(parent, start)
    path_end = get_path_to_com(parent, end)

    # Convert to sets for O(1) lookup
    set_end = set(path_end)

    # Find first common ancestor and its distance from start
    for i, obj in enumerate(path_start):
        if obj in set_end:
            # i is the distance from start's parent to the common ancestor
            # path_end.index(obj) is the distance from end's parent to the same
            return i + path_end.index(obj)

    return -1


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
    print(f"Part 1 Example result: {result} (expected: 42)")
    return result == 42


def run_example2():
    """Test Part 2 with the example from the problem."""
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
K)L
K)YOU
I)SAN"""
    parent = parse_input(example.strip().split('\n'))
    result = min_transfers(parent, 'YOU', 'SAN')
    print(f"Part 2 Example result: {result} (expected: 4)")
    return result == 4


def part1():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')
    parent = parse_input(lines)
    return count_orbits(parent)


def part2():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')
    parent = parse_input(lines)
    return min_transfers(parent, 'YOU', 'SAN')


if __name__ == "__main__":
    print("Testing example Part 1...")
    if run_example():
        print("Part 1 Example passed!")
    else:
        print("Part 1 Example FAILED!")

    print("\nPart 1:", part1())

    print("\nTesting example Part 2...")
    if run_example2():
        print("Part 2 Example passed!")
    else:
        print("Part 2 Example FAILED!")

    print("\nPart 2:", part2())

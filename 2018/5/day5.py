import os
import sys


def react(polymer):
    """Fully react a polymer, returning the final string."""
    stack = []
    for c in polymer:
        if stack and c != stack[-1] and c.lower() == stack[-1].lower():
            # Same letter, opposite case - they react and cancel
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        polymer = f.read().strip()

    result = react(polymer)
    return len(result)


def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        polymer = f.read().strip()

    # Try removing each unit type (a-z) and find minimum length
    best = len(polymer)
    for unit in 'abcdefghijklmnopqrstuvwxyz':
        # Remove all occurrences of this unit (both cases)
        filtered = polymer.replace(unit, '').replace(unit.upper(), '')
        result = react(filtered)
        if len(result) < best:
            best = len(result)

    return best


def run_example():
    """Test with the example from the puzzle."""
    example = "dabAcCaCBAcCcaDA"
    result = react(example)
    print(f"Example: {example}")
    print(f"After reaction: {result}")
    print(f"Length: {len(result)}")
    assert len(result) == 10, f"Expected 10, got {len(result)}"
    print("Example passed!")


if __name__ == "__main__":
    run_example()
    print()
    print("Part 1:", part1())
    print("Part 2:", part2())

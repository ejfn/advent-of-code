import os
import sys


def part1(digits):
    """Sum of all digits that match the next digit (circular list)."""
    total = 0
    n = len(digits)
    for i in range(n):
        if digits[i] == digits[(i + 1) % n]:
            total += int(digits[i])
    return total


def part2(digits):
    """Sum of all digits that match the digit halfway around the circular list."""
    total = 0
    n = len(digits)
    half = n // 2
    for i in range(n):
        if digits[i] == digits[(i + half) % n]:
            total += int(digits[i])
    return total


def run_example():
    # Part 1 examples
    assert part1("1122") == 3
    assert part1("1111") == 4
    assert part1("1234") == 0
    assert part1("91212129") == 9
    print("Part 1 examples passed!")
    
    # Part 2 examples
    assert part2("1212") == 6
    assert part2("1221") == 0
    assert part2("123425") == 4
    assert part2("123123") == 12
    assert part2("12131415") == 4
    print("Part 2 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        digits = f.read().strip()
    
    print(f"Part 1: {part1(digits)}")
    print(f"Part 2: {part2(digits)}")

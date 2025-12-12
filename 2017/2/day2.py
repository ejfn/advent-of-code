import os
import sys


def part1(rows):
    """Sum of differences between max and min of each row."""
    total = 0
    for row in rows:
        total += max(row) - min(row)
    return total


def part2(rows):
    """Sum of the only even division in each row."""
    total = 0
    for row in rows:
        for i, a in enumerate(row):
            for j, b in enumerate(row):
                if i != j and a % b == 0:
                    total += a // b
                    break
            else:
                continue
            break
    return total


def parse_input(text):
    rows = []
    for line in text.strip().split('\n'):
        if line.strip():
            rows.append([int(x) for x in line.split()])
    return rows


def run_example():
    # Part 1 example
    example1 = """5 1 9 5
7 5 3
2 4 6 8"""
    assert part1(parse_input(example1)) == 18
    print("Part 1 example passed!")
    
    # Part 2 example
    example2 = """5 9 2 8
9 4 7 3
3 8 6 5"""
    assert part2(parse_input(example2)) == 9
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        rows = parse_input(f.read())
    
    print(f"Part 1: {part1(rows)}")
    print(f"Part 2: {part2(rows)}")

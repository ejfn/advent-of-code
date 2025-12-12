import os
import sys


def is_valid_triangle(a, b, c):
    """Check if three sides can form a valid triangle."""
    return a + b > c and a + c > b and b + c > a


def parse_input(text):
    """Parse input into list of triangles (each is [a, b, c])."""
    triangles = []
    for line in text.strip().split('\n'):
        if line.strip():
            triangles.append([int(x) for x in line.split()])
    return triangles


def part1(triangles):
    """Count valid triangles read by rows."""
    return sum(1 for t in triangles if is_valid_triangle(*t))


def part2(triangles):
    """Count valid triangles read by columns (groups of 3 rows)."""
    count = 0
    for i in range(0, len(triangles), 3):
        # Read 3 rows at a time
        rows = triangles[i:i+3]
        if len(rows) == 3:
            # For each column
            for col in range(3):
                a, b, c = rows[0][col], rows[1][col], rows[2][col]
                if is_valid_triangle(a, b, c):
                    count += 1
    return count


def run_example():
    # Part 1: 5 10 25 is not a valid triangle
    assert not is_valid_triangle(5, 10, 25)
    assert is_valid_triangle(3, 4, 5)
    print("Part 1 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        triangles = parse_input(f.read())
    
    print(f"Part 1: {part1(triangles)}")
    print(f"Part 2: {part2(triangles)}")

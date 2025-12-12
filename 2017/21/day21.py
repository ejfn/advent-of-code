import os
import sys


def parse_rules(text):
    """Parse enhancement rules into dict."""
    rules = {}
    for line in text.strip().split('\n'):
        if '=>' not in line:
            continue
        left, right = line.split(' => ')
        pattern = tuple(left.split('/'))
        output = tuple(right.split('/'))
        
        # Add all rotations and flips
        for variant in get_variants(pattern):
            rules[variant] = output
    
    return rules


def get_variants(pattern):
    """Get all 8 rotations/flips of a pattern."""
    variants = []
    
    def rotate(p):
        """Rotate 90 degrees clockwise."""
        n = len(p)
        return tuple(''.join(p[n-1-j][i] for j in range(n)) for i in range(n))
    
    def flip(p):
        """Flip horizontally."""
        return tuple(row[::-1] for row in p)
    
    current = pattern
    for _ in range(4):
        variants.append(current)
        variants.append(flip(current))
        current = rotate(current)
    
    return variants


def grid_to_tuple(grid):
    """Convert grid (list of strings) to tuple for hashing."""
    return tuple(grid)


def tuple_to_grid(t):
    """Convert tuple back to list."""
    return list(t)


def split_grid(grid, size):
    """Split grid into smaller squares of given size."""
    n = len(grid)
    squares = []
    
    for row in range(n // size):
        row_squares = []
        for col in range(n // size):
            square = tuple(
                grid[row * size + i][col * size:col * size + size]
                for i in range(size)
            )
            row_squares.append(square)
        squares.append(row_squares)
    
    return squares


def join_grid(squares):
    """Join squares back into a grid."""
    grid = []
    for row_squares in squares:
        square_size = len(row_squares[0])
        for i in range(square_size):
            grid.append(''.join(sq[i] for sq in row_squares))
    return grid


def enhance(grid, rules):
    """Apply one enhancement step."""
    n = len(grid)
    
    if n % 2 == 0:
        size = 2
    else:
        size = 3
    
    squares = split_grid(grid, size)
    new_squares = []
    
    for row in squares:
        new_row = []
        for square in row:
            new_row.append(rules[square])
        new_squares.append(new_row)
    
    return join_grid(new_squares)


def count_on(grid):
    """Count pixels that are on."""
    return sum(row.count('#') for row in grid)


def solve(rules, iterations):
    """Run enhancement for given iterations and count on pixels."""
    grid = ['.#.', '..#', '###']
    
    for _ in range(iterations):
        grid = enhance(grid, rules)
    
    return count_on(grid)


def part1(rules):
    return solve(rules, 5)


def part2(rules):
    return solve(rules, 18)


def run_example():
    example = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
    rules = parse_rules(example)
    assert solve(rules, 2) == 12
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        rules = parse_rules(f.read())
    
    print(f"Part 1: {part1(rules)}")
    print(f"Part 2: {part2(rules)}")

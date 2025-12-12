import os
import sys


def parse_input(text):
    """Parse grid, preserving spaces."""
    lines = text.split('\n')
    # Find max width
    max_width = max(len(line) for line in lines) if lines else 0
    # Pad all lines to same width
    grid = [line.ljust(max_width) for line in lines]
    return grid


def solve(grid):
    """Walk the path, collecting letters. Returns (letters, steps)."""
    if not grid or not grid[0]:
        return "", 0
    
    # Find starting position (| in top row)
    start_col = grid[0].index('|')
    
    r, c = 0, start_col
    dr, dc = 1, 0  # Going down
    letters = []
    steps = 0
    
    while True:
        # Check boundaries
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            break
        
        char = grid[r][c]
        
        if char == ' ':
            # Reached the end
            break
        
        steps += 1
        
        if char.isalpha():
            letters.append(char)
        elif char == '+':
            # Need to turn - find the new direction
            # Try perpendicular directions
            if dr != 0:  # Currently moving vertically, try horizontal
                if c + 1 < len(grid[0]) and grid[r][c + 1] != ' ':
                    dr, dc = 0, 1
                elif c - 1 >= 0 and grid[r][c - 1] != ' ':
                    dr, dc = 0, -1
            else:  # Currently moving horizontally, try vertical
                if r + 1 < len(grid) and grid[r + 1][c] != ' ':
                    dr, dc = 1, 0
                elif r - 1 >= 0 and grid[r - 1][c] != ' ':
                    dr, dc = -1, 0
        
        # Move forward
        r += dr
        c += dc
    
    return ''.join(letters), steps


def part1(grid):
    return solve(grid)[0]


def part2(grid):
    return solve(grid)[1]


def run_example():
    example = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """
    grid = parse_input(example)
    assert part1(grid) == "ABCDEF"
    print("Part 1 example passed!")
    assert part2(grid) == 38
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        grid = parse_input(f.read())
    
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")

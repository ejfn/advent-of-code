import sys
import os
import re

class Screen:
    def __init__(self, width=50, height=6):
        self.width = width
        self.height = height
        # grid[row][col]
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
    
    def rect(self, a, b):
        for r in range(b):
            for c in range(a):
                self.grid[r][c] = '#'
                
    def rotate_row(self, y, by):
        # rotate row y right by 'by'
        row = self.grid[y]
        new_row = ['.'] * self.width
        for i in range(self.width):
            new_pos = (i + by) % self.width
            new_row[new_pos] = row[i]
        self.grid[y] = new_row
        
    def rotate_col(self, x, by):
        # rotate column x down by 'by'
        col = [self.grid[r][x] for r in range(self.height)]
        new_col = ['.'] * self.height
        for i in range(self.height):
            new_pos = (i + by) % self.height
            new_col[new_pos] = col[i]
        
        for r in range(self.height):
            self.grid[r][x] = new_col[r]
            
    def count_lit(self):
        return sum(row.count('#') for row in self.grid)
    
    def display(self):
        for row in self.grid:
            print("".join(row))

def solve(lines, width=50, height=6):
    screen = Screen(width, height)
    
    for line in lines:
        if line.startswith("rect"):
            # rect AxB
            a, b = map(int, line.split()[1].split('x'))
            screen.rect(a, b)
        elif line.startswith("rotate row"):
            # rotate row y=A by B
            match = re.search(r'y=(\d+) by (\d+)', line)
            if match:
                y = int(match.group(1))
                by = int(match.group(2))
                screen.rotate_row(y, by)
        elif line.startswith("rotate column"):
            # rotate column x=A by B
            match = re.search(r'x=(\d+) by (\d+)', line)
            if match:
                x = int(match.group(1))
                by = int(match.group(2))
                screen.rotate_col(x, by)
                
    return screen

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    screen = solve(lines)
    return screen.count_lit()

def part2():
    # Usually requires visual inspection
    print("Part 2 Screen:")
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    screen = solve(lines)
    screen.display()
    return "See output above"

def run_example():
    lines = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1"
    ]
    print("Running example...")
    screen = solve(lines, width=7, height=3)
    screen.display()
    print(f"Lit pixels: {screen.count_lit()}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

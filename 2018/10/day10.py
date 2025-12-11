import sys
import os
import re

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    points = []
    pattern = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            points.append([int(x) for x in match.groups()])
    return points

def get_bounds(points, time):
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    
    for px, py, vx, vy in points:
        x = px + vx * time
        y = py + vy * time
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        
    return min_x, max_x, min_y, max_y

def print_grid(points, time):
    min_x, max_x, min_y, max_y = get_bounds(points, time)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    for px, py, vx, vy in points:
        x = px + vx * time
        y = py + vy * time
        grid[y - min_y][x - min_x] = '#'
        
    for row in grid:
        print("".join(row))

def solve():
    points = parse_input(os.path.join(sys.path[0], 'input.txt'))
    
    min_area = float('inf')
    time = 0
    
    while True:
        min_x, max_x, min_y, max_y = get_bounds(points, time)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        area = width * height
        
        if area < min_area:
            min_area = area
            # Keep going
        else:
            # Area started increasing! The previous one was the minimum.
            # So the message was at time - 1
            print(f"Minimal area found at time={time-1}")
            print_grid(points, time-1)
            print(f"Part 2 Answer: {time-1}")
            return
            
        time += 1

if __name__ == '__main__':
    solve()

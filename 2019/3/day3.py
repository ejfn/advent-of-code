
import os
import sys


def get_points(path_str):
    points = {}
    x, y = 0, 0
    steps = 0
    moves = path_str.split(',')
    for move in moves:
        direction = move[0]
        dist = int(move[1:])
        dx, dy = 0, 0
        if direction == 'R': dx = 1
        elif direction == 'L': dx = -1
        elif direction == 'U': dy = 1
        elif direction == 'D': dy = -1
        
        for _ in range(dist):
            x += dx
            y += dy
            steps += 1
            if (x, y) not in points:
                points[(x, y)] = steps
    return points

def part1(lines):
    wire1_path = lines[0]
    wire2_path = lines[1]
    
    points1 = get_points(wire1_path)
    points2 = get_points(wire2_path)
    
    intersections = set(points1.keys()).intersection(set(points2.keys()))
    
    min_dist = float('inf')
    for x, y in intersections:
        dist = abs(x) + abs(y)
        if dist < min_dist:
            min_dist = dist
            
    return min_dist

def part2(lines):
    wire1_path = lines[0]
    wire2_path = lines[1]
    
    points1 = get_points(wire1_path)
    points2 = get_points(wire2_path)
    
    intersections = set(points1.keys()).intersection(set(points2.keys()))
    
    min_steps = float('inf')
    for p in intersections:
        steps = points1[p] + points2[p]
        if steps < min_steps:
            min_steps = steps
            
    return min_steps

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")

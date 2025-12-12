import sys
import os
from collections import deque

def is_wall(x, y, fav_num):
    val = x*x + 3*x + 2*x*y + y + y*y + fav_num
    # count bits
    bits = bin(val).count('1')
    return bits % 2 != 0

def solve_bfs(fav_num, target_x, target_y):
    # Queue: (x, y, dist)
    queue = deque([(1, 1, 0)])
    visited = set([(1, 1)])
    
    while queue:
        x, y, dist = queue.popleft()
        
        if x == target_x and y == target_y:
            return dist
            
        # Neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if nx < 0 or ny < 0:
                continue
                
            if (nx, ny) in visited:
                continue
                
            if is_wall(nx, ny, fav_num):
                continue
                
            visited.add((nx, ny))
            queue.append((nx, ny, dist + 1))
            
    return -1

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        fav_num = int(f.read().strip())
    
    return solve_bfs(fav_num, 31, 39)

def solve_bfs_part2(fav_num, max_steps):
    queue = deque([(1, 1, 0)])
    visited = set([(1, 1)])
    
    while queue:
        x, y, dist = queue.popleft()
        
        if dist >= max_steps:
            continue
            
        # Neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if nx < 0 or ny < 0:
                continue
                
            if (nx, ny) in visited:
                continue
                
            if is_wall(nx, ny, fav_num):
                continue
                
            visited.add((nx, ny))
            queue.append((nx, ny, dist + 1))
            
    return len(visited)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        fav_num = int(f.read().strip())
    
    return solve_bfs_part2(fav_num, 50)

def run_example():
    fav_num = 10
    target_x, target_y = 7, 4
    steps = solve_bfs(fav_num, target_x, target_y)
    print(f"Example (fav={fav_num} -> {target_x},{target_y}): {steps} steps (expected 11)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

import sys
import os
from collections import deque
from itertools import permutations

def parse_grid(lines):
    grid = []
    pois = {} # Points of Interest
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line.strip()):
            row.append(char)
            if char.isdigit():
                pois[int(char)] = (r, c)
        grid.append(row)
    return grid, pois

def bfs(start_pos, grid):
    # BFS to find distances from start_pos to all other reachable cells
    # Optimization: We only care about distances to other POIs, but full BFS is easy.
    rows = len(grid)
    cols = len(grid[0])
    q = deque([(start_pos, 0)])
    visited = {start_pos}
    dists = {}
    
    while q:
        (r, c), dist = q.popleft()
        
        # Check if this cell is a POI? 
        # Actually just return dict of all reached coords?
        # Or just return distance map for POI locations.
        dists[(r, c)] = dist
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != '#' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append(((nr, nc), dist + 1))
    return dists

def compute_poi_distances(grid, pois):
    # Returns matrix or dict of dists between POIs
    poi_dists = {}
    for p_id, pos in pois.items():
        all_dists = bfs(pos, grid)
        for other_id, other_pos in pois.items():
            if p_id == other_id:
                continue
            if other_pos in all_dists:
                poi_dists[(p_id, other_id)] = all_dists[other_pos]
            else:
                # Unreachable? Should not happen in puzzle input
                pass
    return poi_dists

def solve_tsp(pois, poi_dists, return_to_zero=False):
    # Start at 0
    # Visit all other numbers
    others = [p for p in pois if p != 0]
    min_dist = float('inf')
    
    for perm in permutations(others):
        current_dist = 0
        current_pos = 0
        
        valid = True
        for next_pos in perm:
            if (current_pos, next_pos) in poi_dists:
                current_dist += poi_dists[(current_pos, next_pos)]
                current_pos = next_pos
            else:
                valid = False
                break
        
        if valid:
            if return_to_zero:
                if (current_pos, 0) in poi_dists:
                    current_dist += poi_dists[(current_pos, 0)]
                else:
                    valid = False
            
            if valid:
                min_dist = min(min_dist, current_dist)
                
    return min_dist

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    grid, pois = parse_grid(lines)
    poi_dists = compute_poi_distances(grid, pois)
    return solve_tsp(pois, poi_dists, return_to_zero=False)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    grid, pois = parse_grid(lines)
    poi_dists = compute_poi_distances(grid, pois)
    return solve_tsp(pois, poi_dists, return_to_zero=True)

def run_example():
    raw = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""
    lines = raw.strip().split('\n')
    grid, pois = parse_grid(lines)
    poi_dists = compute_poi_distances(grid, pois)
    
    # "0 to 4 (2 steps)"
    print(f"0->4: {poi_dists.get((0,4))} (Expected 2)")
    # "4 to 1 (4 steps)"
    print(f"4->1: {poi_dists.get((4,1))} (Expected 4)")
    # "1 to 2 (6 steps)"
    print(f"1->2: {poi_dists.get((1,2))} (Expected 6)")
    # "2 to 3 (2 steps)"
    print(f"2->3: {poi_dists.get((2,3))} (Expected 2)")
    
    p1 = solve_tsp(pois, poi_dists, False)
    print(f"Example TSP: {p1} (Expected 14)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

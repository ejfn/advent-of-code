
import sys
import os
from collections import defaultdict

def parse_input(data):
    grid = []
    for line in data.strip().split('\n'):
        grid.append(list(line))
    return grid

def step(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '#':
                        neighbors += 1
                        
            if grid[r][c] == '#':
                if neighbors == 1:
                    new_grid[r][c] = '#'
                else:
                    new_grid[r][c] = '.'
            else: # '.'
                if neighbors == 1 or neighbors == 2:
                    new_grid[r][c] = '#'
                else:
                    new_grid[r][c] = '.'
                    
    return new_grid

def grid_to_tuple(grid):
    return tuple("".join(row) for row in grid)

def calc_biodiversity(grid):
    score = 0
    rows = len(grid)
    cols = len(grid[0])
    power = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                score += power
            power *= 2
    return score

def solve_part1(data):
    grid = parse_input(data)
    seen = set()
    
    while True:
        state = grid_to_tuple(grid)
        if state in seen:
            return calc_biodiversity(grid)
        seen.add(state)
        grid = step(grid)

def get_neighbors_recursive(r, c, level, grids, min_level, max_level):
    # Determine neighbors in the recursive structure.
    # Returns the count of bugs in adjacent tiles
    count = 0
    
    # 4 directions
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        
        # 1. Neighbor is outer level?
        if nr < 0:
            # Up to outer level (level - 1)
            # The tile above current grid is (1, 2) in the outer grid
            if level - 1 >= min_level: # Check boundary if we restrict levels
                if grids[level - 1][1][2] == '#':
                    count += 1
                    
        elif nr >= 5:
            # Down to outer level (level - 1)
            # The tile below current grid is (3, 2)
            if level - 1 >= min_level:
                if grids[level - 1][3][2] == '#':
                    count += 1
                    
        elif nc < 0:
            # Left to outer level (level - 1)
            # The tile left of current grid is (2, 1)
            if level - 1 >= min_level:
                if grids[level - 1][2][1] == '#':
                    count += 1
                    
        elif nc >= 5:
            # Right to outer level (level - 1)
            # The tile right of current grid is (2, 3)
            if level - 1 >= min_level:
                if grids[level - 1][2][3] == '#':
                    count += 1
                    
        # 2. Neighbor is the recursive center (2, 2)?
        elif nr == 2 and nc == 2:
            # Inner level (level + 1)
            # We must check the relevant edge of the inner grid
            if level + 1 <= max_level:
                inner_grid = grids[level + 1]
                
                if dr == 0 and dc == 1: # Moving Right into center
                    # Check left edge of inner grid (col 0)
                    for i in range(5):
                        if inner_grid[i][0] == '#': count += 1
                        
                elif dr == 0 and dc == -1: # Moving Left into center
                    # Check right edge of inner grid (col 4)
                    for i in range(5):
                        if inner_grid[i][4] == '#': count += 1
                        
                elif dr == 1 and dc == 0: # Moving Down into center
                    # Check top edge of inner grid (row 0)
                    for i in range(5):
                        if inner_grid[0][i] == '#': count += 1
                        
                elif dr == -1 and dc == 0: # Moving Up into center
                    # Check bottom edge of inner grid (row 4)
                    for i in range(5):
                        if inner_grid[4][i] == '#': count += 1
                        
        # 3. Normal neighbor
        else:
            if grids[level][nr][nc] == '#':
                count += 1
                
    return count

def solve_part2(data):
    initial_grid = parse_input(data)
    
    # We need to simulate infinite levels.
    # Start with level 0 = input.
    # Levels -1, -2... and 1, 2... are initially empty.
    # But bugs propagate.
    # 200 minutes -> Max propagation is 200 levels up/down? Actually much less usually.
    # Let's use a safe range, e.g., -202 to +202.
    
    # Use a dictionary for sparse grids? Or just list of grids.
    # Access: grids[level][r][c]
    
    levels_range = 300 # Sufficient for 200 steps
    min_level = -levels_range
    max_level = levels_range
    
    # Initialize grids
    # Using dict for grids
    grids = defaultdict(lambda: [['.' for _ in range(5)] for _ in range(5)])
    
    # Load level 0
    grids[0] = initial_grid
    
    for _ in range(200): # 200 minutes
        # We only need to process levels that engage.
        # But iterating a fixed range is easier if not too slow.
        # Range of active levels grows by 1 each step approx.
        # Initial: 0. After 1 step: -1, 0, 1.
        
        # To avoid processing sparse empty levels, we can track min/max active levels.
        # But 200 * 25 is small. 400 levels * 25 tiles = 10000 updates. Fast.
        
        new_grids = defaultdict(lambda: [['.' for _ in range(5)] for _ in range(5)])
        
        # Optimization: only check levels with bugs + neighbors
        # Actually simplest to iterate min_active - 1 to max_active + 1
        
        # Identify active range
        active_levels = sorted([l for l, g in grids.items() if any('#' in row for row in g)])
        if not active_levels:
            current_min, current_max = 0, 0
        else:
            current_min, current_max = active_levels[0], active_levels[-1]
            
        # Process range
        for level in range(current_min - 1, current_max + 2):
            for r in range(5):
                for c in range(5):
                    if r == 2 and c == 2: continue # Center is recursive
                    
                    neighbors = get_neighbors_recursive(r, c, level, grids, min_level, max_level)
                    
                    has_bug = (grids[level][r][c] == '#')
                    
                    if has_bug:
                        if neighbors == 1:
                            new_grids[level][r][c] = '#'
                        else:
                            new_grids[level][r][c] = '.'
                    else:
                        if neighbors == 1 or neighbors == 2:
                            new_grids[level][r][c] = '#'
                        else:
                            new_grids[level][r][c] = '.'
                            
        grids = new_grids

    # Count bugs
    total_bugs = 0
    for g in grids.values():
        for r in range(5):
            for c in range(5):
                if r == 2 and c == 2: continue
                if g[r][c] == '#':
                    total_bugs += 1
                    
    return total_bugs

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

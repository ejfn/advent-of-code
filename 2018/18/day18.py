
import sys
import os
import copy

def parse_input(filename):
    with open(filename, 'r') as f:
        # readlines includes newlines and potentially empty line at end
        # Input looks like 50x50 grid. 
        # Strip newlines from right
        grid = [line.rstrip('\n') for line in f.readlines() if line.strip()]
    return grid

def get_adj(grid, x, y):
    h = len(grid)
    w = len(grid[0])
    adj = []
    trees = 0
    lumber = 0
    open_g = 0
    
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                c = grid[ny][nx]
                if c == '|': trees += 1
                elif c == '#': lumber += 1
                elif c == '.': open_g += 1
                
    return trees, lumber, open_g

def step(grid):
    h = len(grid)
    w = len(grid[0])
    new_grid = [['' for _ in range(w)] for _ in range(h)]
    
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            trees, lumber, open_g = get_adj(grid, x, y)
            
            if c == '.':
                if trees >= 3:
                    new_grid[y][x] = '|'
                else:
                    new_grid[y][x] = '.'
            elif c == '|':
                if lumber >= 3:
                    new_grid[y][x] = '#'
                else:
                    new_grid[y][x] = '|'
            elif c == '#':
                if lumber >= 1 and trees >= 1:
                    new_grid[y][x] = '#'
                else:
                    new_grid[y][x] = '.'
                    
    return ["".join(row) for row in new_grid]

def resource_value(grid):
    trees = sum(row.count('|') for row in grid)
    lumber = sum(row.count('#') for row in grid)
    return trees * lumber

def solve_part1(filename):
    grid = parse_input(filename)
    for _ in range(10):
        grid = step(grid)
    return resource_value(grid)

def solve_part2(filename):
    grid = parse_input(filename)
    # 1,000,000,000 minutes is too long to simulate directly.
    # We must find a cycle.
    
    seen = {}
    history = []
    
    target = 1000000000
    
    for i in range(target):
        # Convert grid to string or tuple for hashing
        state = "\n".join(grid)
        
        if state in seen:
            first_seen_at = seen[state]
            period = i - first_seen_at
            
            remaining = target - i
            offset = remaining % period
            
            # The state at target will be same as state at (first_seen_at + offset)
            # Or just jump ahead
            
            final_idx = first_seen_at + offset
            final_state = history[final_idx]
            
            # Convert back to grid if needed, or just count chars in string
            trees = final_state.count('|')
            lumber = final_state.count('#')
            return trees * lumber
            
        seen[state] = i
        history.append(state)
        
        grid = step(grid)
        
    return resource_value(grid)

def run_example():
    ex = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(ex)
        tmp_name = tmp.name
        
    p1 = solve_part1(tmp_name)
    print(f"Example Part 1: {p1} (Expected 1147)")
    assert p1 == 1147
    print("Example passed!")
    os.remove(tmp_name)

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

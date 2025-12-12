
import sys
import os
import heapq

# Set depth
sys.setrecursionlimit(1000000)

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    depth = int(lines[0].split(': ')[1])
    target_coords = lines[1].split(': ')[1].strip()
    tx, ty = map(int, target_coords.split(','))
    return depth, tx, ty

# Global cache for erosion levels
erosion_cache = {}
depth_val = 0
target_x, target_y = 0, 0

def get_erosion(x, y):
    if (x, y) in erosion_cache:
        return erosion_cache[(x, y)]
    
    geo_idx = 0
    if x == 0 and y == 0:
        geo_idx = 0
    elif x == target_x and y == target_y:
        geo_idx = 0
    elif y == 0:
        geo_idx = x * 16807
    elif x == 0:
        geo_idx = y * 48271
    else:
        geo_idx = get_erosion(x-1, y) * get_erosion(x, y-1)
    
    el = (geo_idx + depth_val) % 20183
    erosion_cache[(x, y)] = el
    return el

def get_type(x, y):
    return get_erosion(x, y) % 3

def solve_part1(filename):
    global depth_val, target_x, target_y, erosion_cache
    depth_val, target_x, target_y = parse_input(filename)
    erosion_cache = {}
    
    # Pre-fill cache iteratively to avoid recursion depth issues for deep targets
    # Fill bounding box 0..tx, 0..ty
    # Row by row
    for x in range(target_x + 1):
        get_erosion(x, 0)
    for y in range(target_y + 1):
        get_erosion(0, y)
        
    for y in range(1, target_y + 1):
        for x in range(1, target_x + 1):
            get_erosion(x, y)
            
    total_risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            risk = get_type(x, y)
            total_risk += risk
            
    return total_risk

def solve_part2(filename):
    global depth_val, target_x, target_y, erosion_cache
    depth_val, target_x, target_y = parse_input(filename)
    erosion_cache = {}
    
    # Types: 0=Rocky, 1=Wet, 2=Narrow
    # Tools: 0=Neither, 1=Climbing, 2=Torch
    # Validation:
    # Rocky(0): {1, 2}
    # Wet(1): {0, 1}
    # Narrow(2): {0, 2}
    allowed_tools = [
        {1, 2}, # Rocky
        {0, 1}, # Wet
        {0, 2}  # Narrow
    ]
    
    start = (0, 0, 2) # x, y, tool
    target = (target_x, target_y, 2)
    
    queue = [(0, 0, 0, 2)] # cost, x, y, tool
    visited = {} # (x, y, tool) -> min_cost
    visited[start] = 0
    
    # Pre-computation strategy:
    # Since we need neighbor erosion levels, we must ensure cache is populated reasonably.
    # But Dijkstra explores locally, so we can lazily compute.
    # However, recursion depth might bite us if we go deep into new territory recursively.
    # Better to expand iteratively if needed?
    # Actually, if we move step by step, we only ask for neighbors.
    # (x, y) needs (x-1, y) and (x, y-1) to compute its erosion.
    # If we explore (100, 100), we probably explored (99, 100) and (100, 99) already?
    # Not necessarily in A*.
    # But `get_erosion` calls recursive steps.
    # If we request (15, 800), it might recurse up to (0, 800) and (15, 0).
    # Since y=763, this is deep.
    # We should ensure we compute iteratively or have a robust way.
    # Since input is narrow (12), maybe we just extend the grid horizontally?
    # But we might go wide to go around walls.
    
    # Let's verify Y depth issue.
    # `get_erosion` recursion for (x, y) depends on (x-1, y) and (x, y-1).
    # Python recursion limit 1M set at top. 
    # For (12, 763), max depth is 12+763 = 775. 1M is plenty.
    
    while queue:
        cost, x, y, tool = heapq.heappop(queue)
        
        if (x, y, tool) == target:
            return cost
        
        if cost > visited.get((x, y, tool), float('inf')):
            continue
            
        region_type = get_type(x, y)
        
        # 1. Switch tool
        for next_tool in allowed_tools[region_type]:
            if next_tool != tool:
                new_cost = cost + 7
                if new_cost < visited.get((x, y, next_tool), float('inf')):
                    visited[(x, y, next_tool)] = new_cost
                    heapq.heappush(queue, (new_cost, x, y, next_tool))
        
        # 2. Move
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue
                
            # Check constraints or bounds?
            # It's infinite, but practically bounded.
            # Don't go excessively far. E.g. x > target_x + 100?
            if nx > target_x + 50 or ny > target_y + 100: # Heuristic bounds
                continue
            
            # To enter nx, ny, tool must be valid there
            n_type = get_type(nx, ny)
            if tool in allowed_tools[n_type]:
                new_cost = cost + 1
                if new_cost < visited.get((nx, ny, tool), float('inf')):
                    visited[(nx, ny, tool)] = new_cost
                    heapq.heappush(queue, (new_cost, nx, ny, tool))
                    
    return -1

def run_example():
    # Mock input
    # depth: 510
    # target: 10,10
    
    import tempfile
    content = "depth: 510\ntarget: 10,10"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(content)
        tmp_name = tmp.name
        
    p1 = solve_part1(tmp_name)
    print(f"Example Part 1: {p1} (Expected 114)")
    assert p1 == 114
    
    p2 = solve_part2(tmp_name)
    print(f"Example Part 2: {p2} (Expected 45)")
    assert p2 == 45
    
    print("Examples passed!")
    os.remove(tmp_name)

if __name__ == '__main__':
    run_example()
    
    import os
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

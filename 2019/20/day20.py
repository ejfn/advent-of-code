
import sys
import os
from collections import deque, defaultdict
import heapq

def parse_maze(data):
    grid = {}
    lines = data.split('\n')
    
    # Store raw lines to easily access chars
    # Max width might vary, assume padded or handle bounds
    
    # Find all letters
    # Portals are two letters.
    # They can be vertical or horizontal.
    # They identify a portal point which is the *adjacent dot*.
    
    # First, load grid into map
    # We strip newlines but keep spaces? Yes spaces are important (void).
    # Actually split('\n') removes newlines.
    
    # Identify portals.
    # Portal labels are outside the maze or inside the donut hole.
    # A label is two uppercase letters.
    # The portal entry point is the dot '.' immediately adjacent to one of the letters.
    
    # Scan for letters.
    letters = {} # (x,y) -> char
    
    max_y = len(lines)
    max_x = max(len(line) for line in lines)
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x,y)] = char
            if 'A' <= char <= 'Z':
                letters[(x,y)] = char
                
    portals = defaultdict(list) # 'AA' -> [(x,y)] of the DOT
    
    # Helper to check if pos is dot
    def is_dot(x, y):
        return grid.get((x,y)) == '.'
    
    # Scan letters to form labels
    for (x,y), char in letters.items():
        # Check if it makes a horizontal label
        # Case 1: char is left part (x, x+1)
        if (x+1, y) in letters:
            label = char + letters[(x+1, y)]
            # Check left of pair or right of pair for dot
            if is_dot(x-1, y):
                portals[label].append((x-1, y))
            elif is_dot(x+2, y):
                portals[label].append((x+2, y))
                
        # Case 2: char is top part (y, y+1)
        if (x, y+1) in letters:
            label = char + letters[(x, y+1)]
            if is_dot(x, y-1):
                portals[label].append((x, y-1))
            elif is_dot(x, y+2):
                portals[label].append((x, y+2))
                
    # portals map: 'BC' -> [(x1,y1), (x2,y2)]
    # 'AA' -> [(sx, sy)]
    # 'ZZ' -> [(ex, ey)]
    
    # Build a lookup for portal jumps
    # (x,y) -> (dest_x, dest_y)
    portal_jumps = {}
    
    start_pos = portals['AA'][0]
    end_pos = portals['ZZ'][0]
    
    for label, points in portals.items():
        if label == 'AA' or label == 'ZZ':
            continue
        if len(points) == 2:
            p1, p2 = points
            portal_jumps[p1] = p2
            portal_jumps[p2] = p1
        else:
            # Should not happen based on description
            pass
            
    return grid, start_pos, end_pos, portal_jumps, portals, max_x, max_y

def solve_part1(data):
    grid, start, end, jumps, _, _, _ = parse_maze(data)
    
    queue = deque([(start, 0)])
    visited = set([start])
    
    while queue:
        (curr_x, curr_y), dist = queue.popleft()
        
        if (curr_x, curr_y) == end:
            return dist
            
        # Neighbors
        # Standard moves
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if grid.get((nx, ny)) == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
                
        # Portal jump
        if (curr_x, curr_y) in jumps:
            dest = jumps[(curr_x, curr_y)]
            if dest not in visited:
                visited.add(dest)
                queue.append((dest, dist + 1)) # Jump takes 1 step
                
    return -1

def bfs_distances(grid, start_pos, pois):
    # Compute dist from start_pos to all reachable POIs
    # pois is a set of coordinates
    distances = {}
    queue = deque([(start_pos, 0)])
    visited = set([start_pos])
    
    while queue:
        (cx, cy), dist = queue.popleft()
        
        if (cx, cy) in pois and (cx, cy) != start_pos:
            distances[(cx, cy)] = dist
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if grid.get((nx, ny)) == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    return distances

def solve_part2(data):
    grid, start, end, jumps, portals_map, width, height = parse_maze(data)
    
    outer_x_min = 3
    outer_x_max = width - 3
    outer_y_min = 3
    outer_y_max = height - 3
    
    # Calculate bounds dynamically based on portal positions
    all_portal_points = set()
    for points in portals_map.values():
        for p in points:
            all_portal_points.add(p)
            
    min_px = min(p[0] for p in all_portal_points)
    max_px = max(p[0] for p in all_portal_points)
    min_py = min(p[1] for p in all_portal_points)
    max_py = max(p[1] for p in all_portal_points)
    
    def is_outer(x, y):
        return x == min_px or x == max_px or y == min_py or y == max_py
    
    # 1. Build POI Graph
    # POIs are Start(AA), End(ZZ), and all Portal points.
    pois = set()
    pois.add(start)
    pois.add(end)
    for p_list in portals_map.values():
        for p in p_list:
            pois.add(p)
            
    # Adjacency list: poi -> [(other_poi, dist), ...]
    # This represents walking on the grid at a single level
    poi_adj = defaultdict(list)
    
    for p in pois:
        dists = bfs_distances(grid, p, pois)
        for target, d in dists.items():
            poi_adj[p].append((target, d))
            
    # 2. Dijkstra on Abstract Graph
    # State: (current_coord, level)
    # Start: (start, 0)
    # End Target: (end, 0)
    
    pq = [(0, start, 0)] # cost, coord, level
    visited = set()
    min_costs = {} # (coord, level) -> cost
    
    # Identify AA and ZZ coordinates
    aa_pos = start
    zz_pos = end
    
    while pq:
        cost, curr, level = heapq.heappop(pq)
        
        if (curr, level) in visited:
            continue
        visited.add((curr, level))
        
        if curr == zz_pos and level == 0:
            return cost
            
        # Optimization: prune if we've found a cheaper way
        if min_costs.get((curr, level), float('inf')) < cost:
            continue
        min_costs[(curr, level)] = cost
        
        # Transitions
        
        # 1. Walk to other POIs on the same level
        for neighbor, walk_dist in poi_adj[curr]:
            # Can only walk to AA or ZZ if level == 0
            if neighbor == aa_pos or neighbor == zz_pos:
                if level != 0:
                    continue
            
            new_cost = cost + walk_dist
            if new_cost < min_costs.get((neighbor, level), float('inf')):
                min_costs[(neighbor, level)] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, level))
        
        # 2. Use Portal (Jump)
        # Only if curr is a portal (and not AA/ZZ, though they are usually not in jumps dict)
        if curr in jumps:
            dest = jumps[curr]
            
            # Determine level change
            if is_outer(curr[0], curr[1]):
                # Outer -> Up (level - 1)
                next_level = level - 1
            else:
                # Inner -> Down (level + 1)
                next_level = level + 1
                
            if next_level >= 0:
                new_cost = cost + 1
                if new_cost < min_costs.get((dest, next_level), float('inf')):
                    min_costs[(dest, next_level)] = new_cost
                    heapq.heappush(pq, (new_cost, dest, next_level))
                    
    return -1

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().rstrip() # Allow trailing newline preservation/strip logic carefully
        
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

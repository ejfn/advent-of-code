
import sys
import os
from collections import deque
import heapq

def parse_input(data):
    grid = {}
    lines = data.strip().split('\n')
    start_pos = None
    keys = {}
    doors = {}
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x,y)] = char
            if char == '@':
                start_pos = (x, y)
            elif 'a' <= char <= 'z':
                keys[char] = (x, y)
            elif 'A' <= char <= 'Z':
                doors[char] = (x, y)
                
    return grid, start_pos, keys, doors

def get_reachable_keys(grid, start, keys_owned):
    # BFS to find all reachable keys from current position
    # Returns list of (key, dist, pos)
    queue = deque([(start, 0)])
    visited = set([start])
    reachable = []
    
    while queue:
        (curr_x, curr_y), dist = queue.popleft()
        
        char = grid.get((curr_x, curr_y))
        
        # If we hit a key we don't own, add to reachable and stop branching this path?
        # Typically we want to know dist to it.
        # But we can continue past it? Actually collecting it changes state.
        # So we just list it as a reachable next state target.
        if 'a' <= char <= 'z' and char not in keys_owned:
            reachable.append((char, dist, (curr_x, curr_y)))
            # Can we pass through it? Yes. So continue BFS?
            # Actually, collecting a key is an "event". 
            # We don't stop BFS, but we record this key.
            # However, for optimization, finding the key is a goal.
            
        # If we hit a door
        if 'A' <= char <= 'Z':
            if char.lower() not in keys_owned:
                continue # Blocked
                
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if (nx, ny) in grid and grid[(nx, ny)] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
                
    return reachable

def solve_part1(data):
    # This is a shortest path problem on a graph of states.
    # State = (current_position, keys_collected_mask)
    # Since keys are few (up to 26), we can use bitmask.
    
    grid, start, keys, doors = parse_input(data)
    all_keys = sorted(keys.keys())
    key_to_bit = {k: i for i, k in enumerate(all_keys)}
    full_mask = (1 << len(all_keys)) - 1
    
    # Pre-compute distances between POIs (start + keys)
    # Since we need to know if doors block the path, simple dist isn't enough.
    # We need to know required keys for edge.
    
    pois = {'@': start}
    pois.update(keys)
    
    adj = {} # (poi_char) -> [(target_poi_char, dist, keys_needed_mask)]
    
    for p_char, p_pos in pois.items():
        # BFS from p_pos to all other POIs
        queue = deque([(p_pos, 0, 0)]) # pos, dist, doors_mask
        visited = set([p_pos])
        
        adj[p_char] = []
        
        while queue:
            (curr_x, curr_y), dist, doors_mask = queue.popleft()
            
            char = grid.get((curr_x, curr_y))
            
            # If valid char and not start
            if char in pois and char != p_char:
                adj[p_char].append((char, dist, doors_mask))
                
            # Update doors mask if current is door
            new_doors_mask = doors_mask
            if 'A' <= char <= 'Z':
                # Assuming door name maps to key bit
                k = char.lower()
                if k in key_to_bit:
                    new_doors_mask |= (1 << key_to_bit[k])
                
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = curr_x + dx, curr_y + dy
                if (nx, ny) in grid and grid[(nx, ny)] != '#' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1, new_doors_mask))
    
    # Dijkstra
    # State: (dist, current_key_char, collected_mask)
    # Start: (0, '@', 0)
    
    pq = [(0, '@', 0)]
    visited_states = {} # (char, mask) -> dist
    
    while pq:
        d, curr, mask = heapq.heappop(pq)
        
        if mask == full_mask:
            return d
            
        if (curr, mask) in visited_states and visited_states[(curr, mask)] <= d:
            continue
        visited_states[(curr, mask)] = d
        
        # Try all reachable neighbors
        for neighbor, dist_to_neighbor, doors_needed in adj[curr]:
            # Check if we can traverse (do we have keys for doors?)
            if (mask & doors_needed) == doors_needed:
                # Yes.
                new_mask = mask
                if 'a' <= neighbor <= 'z':
                    new_mask |= (1 << key_to_bit[neighbor])
                    
                new_dist = d + dist_to_neighbor
                
                if (neighbor, new_mask) not in visited_states or new_dist < visited_states[(neighbor, new_mask)]:
                    heapq.heappush(pq, (new_dist, neighbor, new_mask))
                    
    return -1

def solve_part2(data):
    # Multiple bots.
    # Modify map:
    # ...
    # .@.
    # ...
    # Becomes
    # @#@
    # ###
    # @#@
    
    # The grid is physically split into 4 isolated quadrants (assuming typical input).
    # Each robot collects keys in its quadrant.
    # BUT, a door in quadrant 1 might require a key from quadrant 2.
    # So robots are dependent.
    # State: ((pos1, pos2, pos3, pos4), keys_mask)
    
    grid, start, keys, doors = parse_input(data)
    sx, sy = start
    
    # Update grid
    grid[(sx, sy)] = '#'
    grid[(sx+1, sy)] = '#'
    grid[(sx-1, sy)] = '#'
    grid[(sx, sy+1)] = '#'
    grid[(sx, sy-1)] = '#'
    
    starts = [
        (sx-1, sy-1), (sx+1, sy-1),
        (sx-1, sy+1), (sx+1, sy+1)
    ]
    
    # Re-build adjacency graph
    # POIs: keys + 4 starts
    # We name starts '0', '1', '2', '3'
    
    pois = keys.copy()
    for i, s in enumerate(starts):
        pois[str(i)] = s
        
    all_keys = sorted(keys.keys())
    key_to_bit = {k: i for i, k in enumerate(all_keys)}
    full_mask = (1 << len(all_keys)) - 1
    
    adj = {} 
    
    # BFS from each POI to find reachable other POIs (in same quadrant)
    for p_char, p_pos in pois.items():
        queue = deque([(p_pos, 0, 0)]) 
        visited = set([p_pos])
        adj[p_char] = []
        
        while queue:
            (curr_x, curr_y), dist, doors_mask = queue.popleft()
            
            char = grid.get((curr_x, curr_y))
            if char in pois and char != p_char:
                # Reachable POI
                adj[p_char].append((char, dist, doors_mask))
            
            new_doors_mask = doors_mask
            if 'A' <= char <= 'Z':
                k = char.lower()
                if k in key_to_bit:
                    new_doors_mask |= (1 << key_to_bit[k])
                    
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = curr_x + dx, curr_y + dy
                if (nx, ny) in grid and grid[(nx, ny)] != '#' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1, new_doors_mask))

    # Dijkstra
    # State: (dist, (curr_1, curr_2, curr_3, curr_4), mask)
    # curr_i is char of last visited POI for bot i
    
    initial_pos = ('0', '1', '2', '3')
    pq = [(0, initial_pos, 0)]
    visited_states = {} # (pos_tuple, mask) -> dist
    
    while pq:
        d, current_positions, mask = heapq.heappop(pq)
        
        if mask == full_mask:
            return d
            
        if (current_positions, mask) in visited_states and visited_states[(current_positions, mask)] <= d:
            continue
        visited_states[(current_positions, mask)] = d
        
        # Try moving each bot
        for i, pos_char in enumerate(current_positions):
            # Try to move bot i from pos_char to any neighbor in adj
            for neighbor, dist_to_neighbor, doors_needed in adj.get(pos_char, []):
                # Check doors
                if (mask & doors_needed) == doors_needed:
                    new_mask = mask
                    if 'a' <= neighbor <= 'z':
                        new_mask |= (1 << key_to_bit[neighbor])
                        
                    new_dist = d + dist_to_neighbor
                    
                    new_positions = list(current_positions)
                    new_positions[i] = neighbor
                    new_positions_tuple = tuple(new_positions)
                    
                    if (new_positions_tuple, new_mask) not in visited_states or new_dist < visited_states[(new_positions_tuple, new_mask)]:
                        heapq.heappush(pq, (new_dist, new_positions_tuple, new_mask))
                        
    return -1

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


import sys
import os
import re
import heapq

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    bots = []
    # pos=<23164544,79451234,30509902>, r=54437991
    regex = r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)"
    
    for line in lines:
        m = re.search(regex, line)
        if m:
            x, y, z = map(int, m.groups()[:3])
            r = int(m.group(4))
            bots.append(((x, y, z), r))
            
    return bots

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def solve_part1(filename):
    bots = parse_input(filename)
    # Find strongest
    strongest = max(bots, key=lambda b: b[1])
    s_pos, s_r = strongest
    
    count = 0
    for pos, r in bots:
        if manhattan(pos, s_pos) <= s_r:
            count += 1
            
    return count

def solve_part2(filename):
    bots = parse_input(filename)
    
    # Bounding box of all bots influence?
    # Or just bot centers?
    # Optimal point is likely near dense cluster.
    # Start with box covering all bot ranges.
    
    min_x = min(b[0][0] for b in bots)
    max_x = max(b[0][0] for b in bots)
    min_y = min(b[0][1] for b in bots)
    max_y = max(b[0][1] for b in bots)
    min_z = min(b[0][2] for b in bots)
    max_z = max(b[0][2] for b in bots)
    
    # We use a large size, power of 2
    max_dim = max(max_x - min_x, max_y - min_y, max_z - min_z)
    size = 1
    while size <= max_dim:
        size *= 2
        
    # Queue items: (-count, dist_to_orig, size, x, y, z)
    # x,y,z is the corner with smallest coords
    # We prioritize high count, then low dist
    
    pq = []
    
    # Initial box
    # Count how many bots intersect
    # x, y, z is min corner
    start_x, start_y, start_z = min_x, min_y, min_z
    
    # Helper to count intersections
    def count_intersections(bx, by, bz, bsize):
        c = 0
        # Box ranges: [bx, bx+bsize-1]
        # Dist from bot center to box
        for (bot_x, bot_y, bot_z), r in bots:
            d = 0
            # For each dimension, add distance to interval
            if bot_x < bx: d += bx - bot_x
            elif bot_x > bx + bsize - 1: d += bot_x - (bx + bsize - 1)
            
            if bot_y < by: d += by - bot_y
            elif bot_y > by + bsize - 1: d += bot_y - (by + bsize - 1)
            
            if bot_z < bz: d += bz - bot_z
            elif bot_z > bz + bsize - 1: d += bot_z - (bz + bsize - 1)
            
            if d <= r:
                c += 1
        return c

    initial_count = count_intersections(start_x, start_y, start_z, size)
    # Dist to orig from box: closest point in box to (0,0,0)
    # The box is [start, start + size - 1].
    # Distance is similar logic.
    def dist_to_orig(bx, by, bz, bsize):
        d = 0
        if 0 < bx: d += bx
        elif 0 > bx + bsize - 1: d += -(bx + bsize - 1) # Wait, abs(coord)
        # Correct logic:
        # Interval [L, R]. 
        # If 0 in [L, R], dist is 0.
        # If 0 < L, dist is L.
        # If 0 > R, dist is -R? No, 0 - R = -R. Dist is abs.
        # Actually logic is: max(0, L - 0, 0 - R) = max(0, L, -R).
        
        dx = max(0, bx, -(bx + bsize - 1))
        dy = max(0, by, -(by + bsize - 1))
        dz = max(0, bz, -(bz + bsize - 1))
        return dx + dy + dz

    initial_dist = dist_to_orig(start_x, start_y, start_z, size)
    
    heapq.heappush(pq, (-initial_count, initial_dist, size, start_x, start_y, start_z))
    
    while pq:
        neg_count, dist, sz, x, y, z = heapq.heappop(pq)
        
        if sz == 1:
            return dist # Found single point with max overlap and min dist
        
        # Split
        half = sz // 2
        
        # 8 sub-boxes
        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    nx = x + dx * half
                    ny = y + dy * half
                    nz = z + dz * half
                    
                    cnt = count_intersections(nx, ny, nz, half)
                    dst = dist_to_orig(nx, ny, nz, half)
                    
                    heapq.heappush(pq, (-cnt, dst, half, nx, ny, nz))
                    
    return 0

def run_example():
    # Mock data? Or create logic?
    # Part 1 example provided. Part 2 example provided in text but need multiple bots.
    pass

if __name__ == '__main__':
    import os
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

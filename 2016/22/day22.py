import sys
import os
import re
from collections import deque

class Node:
    def __init__(self, x, y, size, used, avail, use_pct):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.use_pct = use_pct

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.used}/{self.size})"

def parse_nodes(lines):
    nodes = []
    # Filesystem              Size  Used  Avail  Use%
    # /dev/grid/node-x0-y0     92T   73T    19T   79%
    pattern = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
    
    grid = {}
    max_x = 0
    max_y = 0
    
    for line in lines:
        match = pattern.search(line)
        if match:
            x, y, size, used, avail, pct = map(int, match.groups())
            node = Node(x, y, size, used, avail, pct)
            nodes.append(node)
            grid[(x, y)] = node
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            
    return nodes, grid, max_x, max_y

def solve_part1(nodes):
    count = 0
    # O(N^2)
    for a in nodes:
        for b in nodes:
            if a.used == 0:
                continue
            if a == b:
                continue
            if a.used <= b.avail:
                count += 1
    return count

def solve_part2(grid, max_x, max_y):
    # Find empty node
    empty_node = None
    target_node = grid[(max_x, 0)]
    
    walls = set()
    
    # Analyze grid to find walls
    # A wall is a node that implies we can't move data into it?
    # Actually, we move data FROM a node TO empty node.
    # So we can move data from A to Empty if A.Used <= Empty.Size
    # Input analysis:
    # Empty node has Used=0.
    # Most nodes have Used ~60-70T. Size ~80-90T.
    # Large nodes (Walls) have Used > 100T (e.g. 500T).
    # Empty node Size allows receiving ~80-90T.
    # So Walls are nodes where Used > Empty.Size.
    
    # Let's find the empty node first
    for pos, node in grid.items():
        if node.used == 0:
            empty_node = node
            break
            
    # Define threshold based on empty node capacity? 
    # Or just generic rule from problem: A fits in B.
    # But since we are swapping Empty with Neighbor, effectively we move Neighbor data to Empty.
    # So neighbor must fit in Empty.
    # Neighbor.Used <= Empty.Size.
    
    # Dynamic check in BFS or pre-calc walls?
    # Pre-calc walls is safer if there are only static walls.
    # But Empty node moves, so its Size moves?
    # Problem says "instruct a node to move all of its data to an adjacent node... destination has enough space".
    # When we move A to B, A becomes empty. B becomes full.
    # Does B.Size change? No.
    # Does A.Size change? No.
    # But typically in this puzzle, all "normal" nodes fit in all "normal" nodes.
    # The "large" nodes fit nowhere.
    # Let's verify this constraint by scanning.
    
    capacity = empty_node.size
    for pos, node in grid.items():
        if node.used > capacity:
            walls.add(pos)
            
    # BFS State: (empty_x, empty_y, target_data_x, target_data_y)
    start_state = (empty_node.x, empty_node.y, max_x, 0)
    queue = deque([(start_state, 0)])
    visited = {start_state}
    
    while queue:
        (ex, ey, tx, ty), steps = queue.popleft()
        
        if tx == 0 and ty == 0:
            return steps
            
        # Try moving empty node to adjacent cells
        # (ex, ey) is current empty.
        # "Moving empty to neighbor" means moving neighbor data to empty.
        # Valid if neighbor is not wall.
        
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = ex + dx, ey + dy
            
            if 0 <= nx <= max_x and 0 <= ny <= max_y:
                if (nx, ny) in walls:
                    continue
                
                # If we swap empty with target data
                new_tx, new_ty = tx, ty
                if nx == tx and ny == ty:
                    # Target moved to where empty was
                    new_tx, new_ty = ex, ey
                    
                new_state = (nx, ny, new_tx, new_ty)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, steps + 1))
                    
    return -1

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    nodes, _, _, _ = parse_nodes(lines)
    return solve_part1(nodes)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    nodes, grid, max_x, max_y = parse_nodes(lines)
    return solve_part2(grid, max_x, max_y)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

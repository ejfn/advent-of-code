
import sys
import os
from collections import deque, defaultdict

# Adjust recursion depth just in case
sys.setrecursionlimit(20000)

def parse_input(filename):
    with open(filename, 'r') as f:
        regex = f.read().strip()
    return regex[1:-1] # Remove ^ and $

def solve(filename):
    regex = parse_input(filename)
    
    # We will build the graph using coordinates (x, y)
    # Start at (0, 0)
    # A map from (x, y) to set of neighbors
    # Since it's a grid, we can just store distances using BFS as we expand?
    # But branching means we traverse differently.
    # We need to map out the facility first.
    
    # Actually, we can just compute distances directly while traversing the regex?
    # No, because branches might lead to the same room via different paths.
    # The problem says: "shortest path to that room"
    # So we need the graph structure, then BFS for distances.
    
    # Graph: adjacency list
    adj = defaultdict(set)
    
    # We maintain a stack of positions for branching
    # Stack stores (current_x, current_y)
    # Wait, for branching (option1|option2|...), we return to the start of the group
    # for each option. 
    # So we need a stack of "branch points".
    
    pos = (0, 0)
    stack = []
    
    # Regex traversal
    # Since parentheses are nested, stack works naturally.
    # Iterate char by char.
    
    curr_x, curr_y = 0, 0
    
    for char in regex:
        if char == 'N':
            next_x, next_y = curr_x, curr_y - 1
            adj[(curr_x, curr_y)].add((next_x, next_y))
            adj[(next_x, next_y)].add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == 'S':
            next_x, next_y = curr_x, curr_y + 1
            adj[(curr_x, curr_y)].add((next_x, next_y))
            adj[(next_x, next_y)].add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == 'E':
            next_x, next_y = curr_x + 1, curr_y
            adj[(curr_x, curr_y)].add((next_x, next_y))
            adj[(next_x, next_y)].add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == 'W':
            next_x, next_y = curr_x - 1, curr_y
            adj[(curr_x, curr_y)].add((next_x, next_y))
            adj[(next_x, next_y)].add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == '(':
            # Start of a group
            stack.append((curr_x, curr_y))
        elif char == ')':
            # End of a group
            # Pop the branch point
            current = stack.pop()
            # Where do we continue from?
            # From where we ended? No.
            # "Regardless of which option is taken, the route continues from the position it is left at after taking those steps."
            # Actually, `(A|B)C` means `AC` or `BC`.
            # So after `)`, we are at... wait.
            # If `(A|B)`, we end up at end of A or end of B?
            # The regex matches ALL routes.
            # My current logic tracks one path.
            # With `|`, we reset to branch point.
            # With `)`, we ...?
            # Ah, `(` pushes current pos.
            # `|` resets current pos to stack top (but keeps it on stack).
            # `)` pops stack?
            
            # Let's verify. `^N(E|W)N$`
            # 1. N. at (0, -1).
            # 2. (. push (0, -1).
            # 3. E. at (1, -1).
            # 4. |. reset to (0, -1).
            # 5. W. at (-1, -1).
            # 6. ). pop (0, -1). But where are we now?
            # In regex matching, (E|W) means we are at (1, -1) OR (-1, -1).
            # Then N applies to BOTH.
            # This implies we can be at multiple positions simultaneously.
            # But the AoC problem description structure usually implies a simpler DFS/recursiion.
            # "routes ... will take you through every door... mapping out all of these routes"
            # It seems the regex describes the full connectivity.
            # `^N(E|W)N$` means from (0,0) go N(0,-1). Then E(1,-1) OR W(-1,-1).
            # From (1,-1) go N(1,-2). From (-1,-1) go N(-1,-2).
            # Does the regex engine "split" the path?
            # Yes. 
            # In my traversal, just processing char by char won't handle the "state split".
            # I need to handle all active positions?
            
            pass # See logic refinement below
            
        elif char == '|':
            # Option separator.
            # Reset to the start of the group.
            curr_x, curr_y = stack[-1]
            
    # Logic refinement for tracking positions:
    # A recursive function `build_graph(regex_substr, start_positions)`?
    # Or iterative with stack keeping track of where we left off?
    # Actually, standard algorithm for this:
    # Use a stack to save position at `(`.
    # When `|` is encountered, set current position to `stack.top()`.
    # When `)` is encountered, this means end of group.
    # But wait, what if `(A|B)C`?
    # We traverse A, reach end of A.
    # Traverse B, reach end of B.
    # Then traverse C from... BOTH endpoints?
    # Yes.
    # So we simply need to track the current position. 
    # But since it branches, "current position" is a SET of positions?
    # No, the input regex is a single string. When we parse it linearly:
    # We can effectively just `walk`.
    # But `(A|B)C`:
    # We walk A. At `|`, we jump back to start. We walk B.
    # At `)`, where are we? 
    # We need to continue C from ALL endpoints of A and B.
    # How do we represent "ALL endpoints"?
    # Maybe simple recursion is best.
    
    pass

# Recursive approach
# build(index, current_positions) -> new_positions, new_index
# regex is global or passed
    
def build_map(regex):
    adj = defaultdict(set)
    
    # We can use an iterative stack approach where logical flow is maintained
    # But effectively, since it's a map discovery, we just need to add edges.
    
    # "The rest of the regex matches various sequences... Sequences of letters like this always match that exact route in the same order."
    # Basically, we just need to trace all paths.
    
    # Stack stores (start_pos, set_of_end_positions_collected_so_far)
    # When `|`, we add current pos to collected, reset to start_pos.
    # When `)`, we add current pos to collected, and current pos becomes the set of collected.
    # Wait, if current pos becomes a set, future steps must branch from ALL of them.
    # Yes.
    
    # State: set of current positions.
    current_positions = {(0, 0)}
    stack = [] # Stack of (start_positions, collected_end_positions)
    
    for char in regex:
        if char in 'NSEW':
            next_positions = set()
            for x, y in current_positions:
                if char == 'N': nx, ny = x, y - 1
                elif char == 'S': nx, ny = x, y + 1
                elif char == 'E': nx, ny = x + 1, y
                elif char == 'W': nx, ny = x - 1, y
                
                adj[(x, y)].add((nx, ny))
                adj[(nx, ny)].add((x, y))
                next_positions.add((nx, ny))
            current_positions = next_positions
            
        elif char == '(':
            stack.append((current_positions, set()))
            # current_positions remain as is for the first option
            
        elif char == '|':
            # Finish current option
            start_positions, collected_ends = stack[-1]
            collected_ends.update(current_positions)
            # Reset for next option
            current_positions = start_positions
            
        elif char == ')':
            start_positions, collected_ends = stack.pop()
            collected_ends.update(current_positions)
            current_positions = collected_ends
            
    return adj

def solve_part1(filename):
    regex = parse_input(filename)
    adj = build_map(regex)
    
    # BFS for farthest room
    # Start (0, 0)
    # Distances map
    
    dists = {}
    queue = deque([(0, 0, 0)])
    dists[(0, 0)] = 0
    max_dist = 0
    
    while queue:
        x, y, d = queue.popleft()
        if d > max_dist:
            max_dist = d
            
        for nx, ny in adj[(x, y)]:
            if (nx, ny) not in dists:
                dists[(nx, ny)] = d + 1
                queue.append((nx, ny, d + 1))
                
    return max_dist

def solve_part2(filename):
    regex = parse_input(filename)
    adj = build_map(regex)
    
    dists = {}
    queue = deque([(0, 0, 0)])
    dists[(0, 0)] = 0
    count_1000 = 0
    
    while queue:
        x, y, d = queue.popleft()
        if d >= 1000:
            count_1000 += 1
            
        for nx, ny in adj[(x, y)]:
            if (nx, ny) not in dists:
                dists[(nx, ny)] = d + 1
                queue.append((nx, ny, d + 1))
                
    return count_1000

def run_example():
    ex1 = "^WNE$"
    ex2 = "^ENWWW(NEEE|SSE(EE|N))$"
    ex3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    
    # We need to mock file reading
    import tempfile
    
    def test(regex, expected, name):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write(regex)
            tmp_name = tmp.name
        
        try:
            res = solve_part1(tmp_name)
            print(f"{name}: {res} (Expected {expected})")
            assert res == expected
        finally:
            os.remove(tmp_name)

    test(ex1, 3, "Ex1")
    test(ex2, 10, "Ex2")
    test(ex3, 18, "Ex3")
    print("Examples passed!")

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

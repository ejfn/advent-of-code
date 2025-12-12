
import sys
import os

# Increase recursion depth
sys.setrecursionlimit(20000)

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    clay = set()
    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split(', ')
        first = parts[0].split('=')
        second = parts[1].split('=')
        if first[0] == 'x':
            x_range = [int(first[1]), int(first[1])]
            y_range = list(map(int, second[1].split('..')))
        else:
            y_range = [int(first[1]), int(first[1])]
            x_range = list(map(int, second[1].split('..')))
            
        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                clay.add((x, y))
                
    return clay

def solve(filename):
    clay = parse_input(filename)
    if not clay: return 0, 0
    
    min_y = min(y for x, y in clay)
    max_y = max(y for x, y in clay)
    
    settled = set()
    flowing = set()
    
    def fall(x, y):
        if y > max_y:
            return False # Flows to infinity
        
        if (x, y) in clay or (x, y) in settled:
            return True # Blocked
            
        if (x, y) in flowing:
            # We are revisiting a flowing node.
            # This usually means we are scanning horizontally and encountered a previous flow path?
            # Or vertical overlap?
            # In purely vertical fallback, this shouldn't happen unless cycle (impossible)
            # or joining flow.
            # If joining flow, treating it as "not blocked" (False) is risky?
            # If implies it flows out.
            return False 
            
        # Mark as flowing
        flowing.add((x, y))
        
        # Check down
        blocked_below = fall(x, y + 1)
        
        if not blocked_below:
            return False
            
        # If blocked below, spread
        blocked_left = False
        blocked_right = False
        
        # Scan Left
        lx = x
        while True:
            if (lx - 1, y) in clay or (lx - 1, y) in settled:
                blocked_left = True
                break
            
            # Check if current lx is supported
            # We know lx is supported because we started at x (supported) and moved left
            # But we must check support of neighbors
            
            # Actually, standard logic:
            # Move left. Check if wall.
            # Check if drop.
            
            # Check support BELOW (lx - 1)
            # Wait, support is at y+1
            
            # Flow into (lx-1, y)
            if (lx - 1, y) not in flowing:
                flowing.add((lx - 1, y))
            
            support = fall(lx - 1, y + 1)
            if not support:
                blocked_left = False
                break
            
            lx -= 1
            
        # Scan Right
        rx = x
        while True:
            if (rx + 1, y) in clay or (rx + 1, y) in settled:
                blocked_right = True
                break
            
            if (rx + 1, y) not in flowing:
                flowing.add((rx + 1, y))
                
            support = fall(rx + 1, y + 1)
            if not support:
                blocked_right = False
                break
            
            rx += 1
            
        if blocked_left and blocked_right:
            # Settle range [lx, rx]
            # Note: lx is the last valid water tile, rx is last valid water tile
            # Wait, my loop logic:
            # Left loop: if wall at lx-1, break. so lx is water.
            # If drop at lx-1, break. so lx-1 is NOT water? 
            # In loop: `flowing.add((lx-1, y))`.
            # If drop at lx-1, support=False. break.
            # So lx-1 IS water (flowing).
            # But it spills.
            # So for SETTLING, we should only settle if bounded walls.
            # My current logic: blocked_left=False if drop.
            # So we won't settle.
            # This is correct.
            
            # If settling, we convert flowing to settled
            # The range is tricky based on loop values.
            # Re-re-verify loops.
            
            # Correct scan usually:
            # Find extent left [lx, x]. 
            # lx is the leftmost WATER tile.
            # If (lx-1) is wall -> bounded left.
            # If (lx) has no support -> unbounded left.
            
            # My loop:
            # Decrement lx AFTER checking support of (lx-1)? No.
            
            # Let's clean up scan.
            
            # Scan left
            l_wall = False
            lx = x
            while True:
                # Check wall
                if (lx - 1, y) in clay or (lx - 1, y) in settled:
                    l_wall = True
                    break
                
                # Check drop
                if not fall(lx - 1, y + 1):
                   # Spills
                   lx -= 1 # Ensure this tile is marked flowing? fall() marks it?
                           # fall(lx-1, y+1) marks y+1. what about (lx-1, y)?
                           # We must mark (lx-1, y) as flowing path to drop.
                   flowing.add((lx - 1, y))
                   l_wall = False
                   break
                
                lx -= 1
                flowing.add((lx, y))
                
            # Scan right
            r_wall = False
            rx = x
            while True:
                if (rx + 1, y) in clay or (rx + 1, y) in settled:
                    r_wall = True
                    break
                
                if not fall(rx + 1, y + 1):
                    rx += 1
                    flowing.add((rx, y))
                    r_wall = False
                    break
                
                rx += 1
                flowing.add((rx, y))
                
            if l_wall and r_wall:
                for i in range(lx, rx + 1):
                    settled.add((i, y))
                    # flowing.discard((i, y)) # Optional but cleaner
                return True # Now blocked
            
            return False # Spills
            
    try:
        fall(500, 0)
    except RecursionError:
        print("Recursion limit hit")
        return 0, 0
        
    final_flowing = { (x, y) for (x, y) in flowing if min_y <= y <= max_y and (x, y) not in settled }
    final_settled = { (x, y) for (x, y) in settled if min_y <= y <= max_y }
    
    return len(final_flowing) + len(final_settled), len(final_settled)

def run_example():
    ex = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(ex)
        tmp_name = tmp.name
        
    p1, p2 = solve(tmp_name)
    print(f"Example Part 1: {p1} (Expected 57)")
    print(f"Example Part 2: {p2} (Expected 29)")
    
    os.remove(tmp_name)
    assert p1 == 57
    assert p2 == 29
    print("Example passed!")

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    p1, p2 = solve(input_file)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

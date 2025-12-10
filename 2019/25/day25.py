
import sys
import os
from collections import defaultdict, deque
import itertools
import re

class IntcodeComputer:
    def __init__(self, program):
        self.memory = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        self.pc = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = deque()
        self.halted = False
        self.waiting_for_input = False

    def get_addr(self, pos, mode):
        if mode == 0: return self.memory[pos]
        elif mode == 1: return pos
        elif mode == 2: return self.memory[pos] + self.relative_base
        else: raise ValueError(f"Unknown mode {mode}")

    def get_val(self, pos, mode):
        return self.memory[self.get_addr(pos, mode)]

    def set_val(self, pos, mode, val):
        self.memory[self.get_addr(pos, mode)] = val

    def add_input(self, val):
        self.inputs.append(val)
        self.waiting_for_input = False
    
    def add_ascii_input(self, s):
        for char in s:
            self.inputs.append(ord(char))
    
    def has_output(self):
        return len(self.outputs) > 0
    
    def get_output(self):
        return self.outputs.popleft() if self.outputs else None
    
    def run_until_output_or_input(self):
        while True:
            instr = self.memory[self.pc]
            opcode = instr % 100
            modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

            if opcode == 99:
                self.halted = True
                return 'HALT'
            elif opcode == 1:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], v1 + v2)
                self.pc += 4
            elif opcode == 2:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], v1 * v2)
                self.pc += 4
            elif opcode == 3:
                if not self.inputs:
                    self.waiting_for_input = True
                    return 'INPUT'
                self.set_val(self.pc + 1, modes[0], self.inputs.popleft())
                self.pc += 2
            elif opcode == 4:
                self.outputs.append(self.get_val(self.pc + 1, modes[0]))
                self.pc += 2
                return 'OUTPUT'
            elif opcode == 5:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.pc = v2 if v1 != 0 else self.pc + 3
            elif opcode == 6:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.pc = v2 if v1 == 0 else self.pc + 3
            elif opcode == 7:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], 1 if v1 < v2 else 0)
                self.pc += 4
            elif opcode == 8:
                v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], 1 if v1 == v2 else 0)
                self.pc += 4
            elif opcode == 9:
                self.relative_base += self.get_val(self.pc + 1, modes[0])
                self.pc += 2
            else:
                raise ValueError(f"Unknown opcode {opcode}")

def run_command(computer, cmd):
    if cmd:
        computer.add_ascii_input(cmd + "\n")
    
    output_chars = []
    while True:
        status = computer.run_until_output_or_input()
        if status == 'OUTPUT':
            output_chars.append(chr(computer.get_output()))
        elif status == 'INPUT':
            break
        elif status == 'HALT':
            break
            
    return "".join(output_chars)

def parse_room_name(text):
    for line in text.splitlines():
        if line.startswith('== '):
            return line.strip('= ')
    return None

def parse_items(text):
    items = []
    lines = text.splitlines()
    in_items = False
    for line in lines:
        if line.startswith('Items here:'):
            in_items = True
            continue
        if in_items:
            if line.startswith('- '):
                items.append(line[2:])
            elif line.strip() == '':
                in_items = False
    return items

def parse_doors(text):
    doors = []
    lines = text.splitlines()
    in_doors = False
    for line in lines:
        if line.startswith('Doors here lead:'):
            in_doors = True
            continue
        if in_doors:
            if line.startswith('- '):
                doors.append(line[2:])
            elif line.strip() == '':
                in_doors = False
    return doors

def solve(program):
    computer = IntcodeComputer(program)
    
    # DFS Mapping
    visited = set()
    adj = defaultdict(dict) # room -> {dir -> next_room}
    room_items = {} # room -> [item]
    dangerous_items = ["infinite loop", "giant electromagnet", "molten lava", "photons", "escape pod"]
    reverse_dir = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    
    out = run_command(computer, "")
    start_room = parse_room_name(out)
    
    # Identify checkpoint and pressure floor dir
    checkpoint_room = "Security Checkpoint"
    pressure_dir = None
    
    def dfs(current_room, description):
        visited.add(current_room)
        
        items = parse_items(description)
        doors = parse_doors(description)
        room_items[current_room] = [i for i in items if i not in dangerous_items]
        
        for d in doors:
            # Check if we already know where this leads
            if d in adj[current_room]:
                known_next = adj[current_room][d]
                # If we haven't visited known_next, we should?
                # But in DFS we usually only traverse edges to unvisited.
                # However, we must physically move to traverse.
                
                # If we already connected it, we assume we visited it or will visit?
                # Actually, simple DFS on graph:
                if known_next not in visited:
                     res = run_command(computer, d)
                     dfs(known_next, res)
                     # Backtrack
                     run_command(computer, reverse_dir[d])
                continue
            
            # Unknown edge, explore
            res = run_command(computer, d)
            
            # Check for bounce (pressure floor)
            if "Alert!" in res or "heavier" in res or "lighter" in res:
                # We bounced back to current_room (or stayed in Checkpoint)
                # We know this direction leads to Pressure Floor
                if current_room == checkpoint_room:
                    # Found it
                    pass
                # Don't recurse, don't backtrack (we were pushed back)
                continue
                
            next_room = parse_room_name(res)
            
            if next_room:
                adj[current_room][d] = next_room
                adj[next_room][reverse_dir[d]] = current_room
                
                if next_room not in visited:
                    dfs(next_room, res)
                
                # Backtrack
                run_command(computer, reverse_dir[d])
            else:
                # Should not happen if normal move
                pass

    dfs(start_room, out)
    
    # Mapping done. Now we have exact map.
    # Collect all safe items.
    
    # Re-start for clean state collection
    # (Or we could have collected during DFS, but state management is trickier)
    # Fast path: BFS on `adj` to find items.
    
    # Build graph for BFS
    # adj is ready.
    
    def bfs_path(start, target):
        q = deque([(start, [])])
        seen = {start}
        while q:
            curr, path = q.popleft()
            if curr == target:
                return path
            for d, neighbor in adj[curr].items():
                if neighbor not in seen:
                    seen.add(neighbor)
                    q.append((neighbor, path + [d]))
        return None

    # Collect items
    # Start fresh computer?
    # Actually we can just continue using `computer`? 
    # It is currently at `start_room` (because DFS backtracked all the way).
    # Yes, DFS ends at start.
    
    current_loc = start_room
    
    all_safe_items = []
    for r, items_in_room in room_items.items():
        for item in items_in_room:
            all_safe_items.append((r, item))
            
    for room, item in all_safe_items:
        # Go to room
        path = bfs_path(current_loc, room)
        for move in path:
            run_command(computer, move)
        # Take item
        run_command(computer, f"take {item}")
        current_loc = room
        
    # Go to Security Checkpoint
    path_to_cp = bfs_path(current_loc, checkpoint_room)
    for move in path_to_cp:
        run_command(computer, move)
    current_loc = checkpoint_room
    
    # Identify pressure floor direction
    # It's the direction NOT in adj? Or check exits again.
    # We scanned all doors in DFS. Including the one that bounced.
    # If the one that bounced wasn't added to `adj`, we need to find which one it was.
    # Re-scan current output or check missing connections.
    
    # Get current description again
    desc = run_command(computer, "inv") # Just to flush or get status? No inv just lists items.
    # We need to look implies doors.
    # `adj[checkpoint_room]` has safe exits.
    # We need the unsafe one.
    
    # Just try all 4 dirs. The one not in adj is likely it, or the one that gives alert.
    # But if we encountered it in DFS, we didn't add it to adj.
    
    all_dirs = ['north', 'south', 'east', 'west']
    pressure_dir = None
    
    # Try dirs not in adj[checkpoint_room]
    # But wait, parse_doors gave us the list of doors.
    # DFS iterated them.
    # If we failed to enter (alert), we didn't add to adj.
    # So we just need to try the door that is physically there but not map-connected.
    # Or just try all valid doors from description.
    
    # Look to get description
    look_out = run_command(computer, "look") # Assuming 'look' works? Or just move back and forth?
    # 'look' is not standard.
    # We can infer from `adj`.
    # But we need to know which of the 4 directions IS the pressure floor.
    # In DFS, we tried all doors.
    # If we didn't record one, it's because it alerted.
    # So finding the direction that triggers alert is safe.
    
    for d in all_dirs:
        # If we know this leads to a room, skip (safe for efficiency)
        if d in adj[checkpoint_room]:
            continue
            
        # Try it
        res = run_command(computer, d)
        if "Alert" in res or "heavier" in res or "lighter" in res:
            pressure_dir = d
            break
        # If we moved successfully (e.g. into unknown room not found in DFS? Unlikely), go back
        if parse_room_name(res):
             run_command(computer, reverse_dir[d])
             
    if not pressure_dir:
        # Maybe we processed all in DFS but didn't mark pressure?
        # Fallback: try all dirs
        pass

    # Gray Code
    items = [i[1] for i in all_safe_items]
    n = len(items)
    
    # Current state: Holding ALL items.
    # Try current
    res = run_command(computer, pressure_dir)
    if "Analysis complete! You may proceed." in res:
        return parse_code(res)
        
    # Bitmask: 1 = Hold, 0 = Drop
    # Start: 111...1 (All items held)
    current_mask = (1 << n) - 1
    
    # Gray code usually starts from 0. We are at max.
    # We can iterate from 0 to 2^n, map to mask, diff with current.
    # Or just standard gray code sequence relative to current?
    # Gray code: 0, 1, 3, 2, 6... (change one bit at a time)
    # We want to visit all 2^n states.
    
    # Let's generate standard Gray code sequence 0..(2^n-1)
    # And convert to set of items to hold.
    # Then diff with current inventory.
    
    gray_codes = []
    for i in range(1 << n):
        gray_codes.append(i ^ (i >> 1))
        
    # We are currently at mask (1<<n)-1.
    # We can jump to nearest gray code?
    # No, just drop all first? NO, dropping all is slow.
    # We want one op per step.
    
    # Just standard Gray code from 0?
    # Start with all dropped?
    # Drop all now.
    for item in items:
        run_command(computer, f"drop {item}")
    current_mask = 0
    
    # Iterate gray codes
    for g in gray_codes:
        if g == 0: continue # Empty, checked? Or just skip.
        
        # Diff between current_mask and g
        diff = current_mask ^ g
        # Find bit
        bit = 0
        while (diff >> bit) & 1 == 0:
            bit += 1
        
        item = items[bit]
        if (g >> bit) & 1:
            # New state has bit set -> Take
            run_command(computer, f"take {item}")
        else:
            # New state has bit unset -> Drop
            run_command(computer, f"drop {item}")
            
        current_mask = g
        
        # Try
        res = run_command(computer, pressure_dir)
        if "Analysis complete! You may proceed." in res:
            return parse_code(res)
            
    return "Failed"

def parse_code(text):
    match = re.search(r'\d+', text)
    if match:
        return match.group(0)
    return text

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve(list(program)))

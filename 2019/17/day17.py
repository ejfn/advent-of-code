
import sys
import os
from collections import defaultdict, deque

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
        self.inputs.append(10) # Newline if mostly required, check later? Usually yes.

    def has_output(self):
        return len(self.outputs) > 0
    
    def get_output(self):
        return self.outputs.popleft() if self.outputs else None
    
    def get_all_outputs(self):
        out = list(self.outputs)
        self.outputs.clear()
        return out

    def run(self):
        while True:
            instr = self.memory[self.pc]
            opcode = instr % 100
            modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

            if opcode == 99:
                self.halted = True
                return
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
                    return # Suspends execution waiting for input
                self.set_val(self.pc + 1, modes[0], self.inputs.popleft())
                self.pc += 2
            elif opcode == 4:
                self.outputs.append(self.get_val(self.pc + 1, modes[0]))
                self.pc += 2
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

def parse_grid(outputs):
    grid_str = ''.join(chr(c) for c in outputs)
    lines = grid_str.strip().split('\n')
    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x,y)] = char
    return grid, len(lines[0]), len(lines)

def solve_part1(program):
    computer = IntcodeComputer(program)
    computer.run()
    outputs = computer.get_all_outputs()
    
    grid, width, height = parse_grid(outputs)
    
    alignment_sum = 0
    
    # Intersections are # surrounded by # on all 4 sides
    for (x, y), char in grid.items():
        if char == '#' and x > 0 and x < width - 1 and y > 0 and y < height - 1:
            if (grid.get((x-1, y)) == '#' and 
                grid.get((x+1, y)) == '#' and 
                grid.get((x, y-1)) == '#' and 
                grid.get((x, y+1)) == '#'):
                alignment_sum += x * y
                
    return alignment_sum

def solve_part2(program):
    # Wake up the robot: address 0 = 2
    program[0] = 2
    computer = IntcodeComputer(program)
    
    # We need to construct the movement program.
    # First, run Part 1 logic to get the map.
    program_orig = list(program)
    program_orig[0] = 1 # Just to get map or use backup
    # Actually just re-run Part 1 logic on copy to extract path
    
    # Extract path
    # Find start
    # Traverse until end
    
    # This is manual path compression problem. 
    # For automated solution, we need to trace the path and then compress into A,B,C routines.
    
    # 1. Get Map
    # 2. Trace Path
    # 3. Compress Path
    # 4. Feed Input
    
    pass 
    # Since I cannot see the map yet, I will write the compressor later or
    # write a generic solver now.
    
    # Generic solver:
    # 1. Computer runs, outputs prompt "Main:"
    # 2. We skip prompts for now, just prep inputs.
    
    # Let's get the path first.
    # Re-run getting map
    c_map = IntcodeComputer(program)
    c_map.memory[0] = 1 # Part 1 mode to get map? Does it output map in Part 2?
    # Usually Part 2 waits for input.
    # Let's just use part1 to get map.
    c_map = IntcodeComputer(list(program)) # Reset
    c_map.memory[0] = 1 # Force view
    c_map.run()
    grid, width, height = parse_grid(c_map.get_all_outputs())
    
    # Find start
    start_pos = None
    direction = None # 0=N, 1=E, 2=S, 3=W
    for pos, char in grid.items():
        if char in '^>v<':
            start_pos = pos
            if char == '^': direction = 0
            elif char == '>': direction = 1
            elif char == 'v': direction = 2
            elif char == '<': direction = 3
    
    # Extract path
    path = []
    curr = start_pos
    curr_dir = direction
    moves_count = 0
    
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] # N, E, S, W
    
    while True:
        # Check forward
        dx, dy = directions[curr_dir]
        nx, ny = curr[0] + dx, curr[1] + dy
        if grid.get((nx, ny)) == '#':
            moves_count += 1
            curr = (nx, ny)
        else:
            if moves_count > 0:
                path.append(str(moves_count))
                moves_count = 0
            
            # Turn left or right?
            left_dir = (curr_dir - 1) % 4
            ldx, ldy = directions[left_dir]
            rx, ry = curr[0] + ldx, curr[1] + ldy
            
            right_dir = (curr_dir + 1) % 4
            rdx, rdy = directions[right_dir]
            rx2, ry2 = curr[0] + rdx, curr[1] + rdy
            
            if grid.get((rx, ry)) == '#':
                path.append('L')
                curr_dir = left_dir
            elif grid.get((rx2, ry2)) == '#':
                path.append('R')
                curr_dir = right_dir
            else:
                # Dead end
                break
                
    full_path_str = ",".join(path)
    # Compress path
    # Naive compression: Try all A, B, C lengths (max 20 chars each)
    
    # path is like ['R', '8', 'R', '8', ...]
    # We need to group them. "R,8" is one command technically? 
    # "Movement functions may each contain at most 20 characters, not counting the newline."
    # So "R,8" takes 3 chars.
    
    # Brute force split
    # A can be first k items of path
    # Then replace all A occurences
    # B can be next m items
    # etc.
    
    # Let's tokenize commands as strings "R,8"
    # Actually path is mixed "L", "10", etc.
    # Group turn+move? Prompt says "L,10" etc.
    
    # The list `path` is ['R', '8', 'L', '10', ...]
    # Let's group pairs? usually it's Turn, Move.
    # path elements are alternating Turn, Move (except start? no, first is Turn)
    
    commands = []
    for i in range(0, len(path), 2):
        commands.append(f"{path[i]},{path[i+1]}")
        
    # Now find repeating patterns in `commands` list
    # A, B, C.
    
    def solve_compression(cmds):
        n = len(cmds)
        for len_a in range(1, 11): # Max 20 chars -> rough max 10 commands? "R,12," is 5 chars. So 4 commands is 20 chars approx.
            # A candidate
            cand_a = cmds[:len_a]
            str_a = ",".join(cand_a)
            if len(str_a) > 20: break
            
            # Remove A from start and find next gap for B
            # We can construct a regex or just iterative replacement simulation
            
            # Helper to check if list starts with sublist
            def starts_with(lst, sub):
                if len(lst) < len(sub): return False
                return lst[:len(sub)] == sub
                
            # Recursive solver?
            
            # Remove all A from start?
            # Main logic sequence must be A, B, C calls.
            # So start must be A (or B or C, but we can define first chunk as A).
            
            # Actually, main routine structure is unknown. But typically starts with A.
            
            # Let's try to parse:
            
            rem_after_a = []
            idx = 0
            while idx < n:
                if starts_with(cmds[idx:], cand_a):
                    idx += len_a # Skip A
                else:
                    rem_after_a = cmds[idx:] # Found start of B?
                    break
            
            if not rem_after_a: continue # Consumed all with A? Unlikely but possible
            
            for len_b in range(1, 11):
                cand_b = rem_after_a[:len_b]
                str_b = ",".join(cand_b)
                if len(str_b) > 20: break
                
                # Check A and B
                rem_after_b = []
                idx2 = 0
                valid_ab = True
                while idx2 < n:
                    if starts_with(cmds[idx2:], cand_a):
                        idx2 += len_a
                    elif starts_with(cmds[idx2:], cand_b):
                        idx2 += len_b
                    else:
                        rem_after_b = cmds[idx2:] # Start of C
                        break
                
                if not rem_after_b: 
                    # Solved with only A and B?
                    # valid
                    return cand_a, cand_b, []
                
                for len_c in range(1, 11):
                    cand_c = rem_after_b[:len_c]
                    str_c = ",".join(cand_c)
                    if len(str_c) > 20: break
                    
                    # Verify full coverage
                    main_routine = []
                    idx3 = 0
                    possible = True
                    while idx3 < n:
                        if starts_with(cmds[idx3:], cand_a):
                            main_routine.append('A')
                            idx3 += len_a
                        elif starts_with(cmds[idx3:], cand_b):
                            main_routine.append('B')
                            idx3 += len_b
                        elif starts_with(cmds[idx3:], cand_c):
                            main_routine.append('C')
                            idx3 += len_c
                        else:
                            possible = False
                            break
                    
                    if possible and len(",".join(main_routine)) <= 20:
                        return cand_a, cand_b, cand_c, main_routine
                        
        return None
        
    res = solve_compression(commands)
    if not res:
        print("Failed to compress path")
        return 0
        
    A_cmds, B_cmds, C_cmds, Main_cmds = res
    
    input_str = ""
    input_str += ",".join(Main_cmds) + "\n"
    input_str += ",".join(A_cmds) + "\n"
    input_str += ",".join(B_cmds) + "\n"
    input_str += ",".join(C_cmds) + "\n"
    input_str += "n\n" # Continuous video feed?
    
    # Run robot
    computer = IntcodeComputer(program) # Uses modified program[0]=2
    
    # We need to feed ASCII input
    for char in input_str:
        computer.add_input(ord(char))
        
    computer.run()
    return computer.outputs[-1]

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(program))
    print("Part 2:", solve_part2(program))

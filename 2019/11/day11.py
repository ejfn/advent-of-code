
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

    def has_output(self):
        return len(self.outputs) > 0
    
    def get_output(self):
        return self.outputs.popleft() if self.outputs else None

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
                    return
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

def run_robot(program, start_color=0):
    computer = IntcodeComputer(program)
    grid = defaultdict(int) # 0=black, 1=white
    if start_color == 1:
        grid[(0,0)] = 1
        
    painted = set()
    x, y = 0, 0
    dx, dy = 0, -1 # Start facing Up
    
    while not computer.halted:
        current_color = grid[(x,y)]
        computer.add_input(current_color)
        computer.run()
        
        if computer.has_output():
            color_to_paint = computer.get_output()
            grid[(x,y)] = color_to_paint
            painted.add((x,y))
            
            if computer.has_output():
                turn_direction = computer.get_output() # 0=left, 1=right
                if turn_direction == 0: # Left
                    dx, dy = dy, -dx
                else: # Right
                    dx, dy = -dy, dx
                    
                x += dx
                y += dy
            else:
                # Should not happen based on problem description (outputs come in pairs)
                break
        else:
            if computer.waiting_for_input and not computer.halted:
                # Should have been handled by the loop start adding input
                pass
                
    return grid, painted

def solve_part1(program):
    grid, painted = run_robot(program, start_color=0)
    return len(painted)

def solve_part2(program):
    grid, painted = run_robot(program, start_color=1)
    
    # Render
    if not grid:
        return ""
        
    xs = [pos[0] for pos in grid if grid[pos] == 1]
    ys = [pos[1] for pos in grid if grid[pos] == 1]
    
    if not xs:
        return "No white pixels"
        
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    output = []
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if grid[(x,y)] == 1:
                row += "#"
            else:
                row += " "
        output.append(row)
        
    return "\n" + "\n".join(output)

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(program))
    print("Part 2:", solve_part2(program))

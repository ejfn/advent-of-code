
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

def check_point(program, x, y):
    computer = IntcodeComputer(program)
    computer.add_input(x)
    computer.add_input(y)
    computer.run()
    return computer.get_output()

def solve_part1(program):
    count = 0
    for y in range(50):
        for x in range(50):
            if check_point(program, x, y):
                count += 1
    return count

def solve_part2(program):
    # We need to find the top-left corner of a 100x100 square that fits entirely within the beam.
    # The beam is generally defined by lower and upper lines y = mx.
    # We can trace the edges.
    
    # We need to find (x, y) such that:
    # (x, y) is in beam
    # (x+99, y) is in beam
    # (x, y+99) is in beam
    # (x+99, y+99) is in beam (implied by convexity if the others are?)
    
    # Actually, if we find (x, y) such that (x+99, y) is in beam, and (x, y+99) is in beam...
    # Wait, the square must fit IN the beam. 
    # The beam widens as we go further.
    # So we want the closest point such that the square fits.
    
    # Let's track the beam's width and position.
    # For a given Y, finding the range of X (x_start, x_end) that is in the beam.
    # The beam is continuous in X for a given Y.
    
    y = 100
    x = 0
    
    while True:
        # Find start of beam at this Y (assuming beam moves right/down)
        while check_point(program, x, y) == 0:
            x += 1
            
        # Beam starts at x.
        # Check if the square fits.
        # Top-left is (x, y - 99)? No, we iterate y downwards (increasing y).
        # We want top-left (x_tl, y_tl) of the square.
        # Let's say current row is the BOTTOM row of the square (y).
        # And the beam starts at x (bottom-left of square).
        # Then we check if the top-right of the square (x + 99, y - 99) is in the beam.
        
        # Why this way? Because we march Y forward.
        # If we are at row y, and beam starts at x,
        # we can put a square's bottom-left at (x, y). 
        # Then top-left is (x, y-99). Top-right is (x+99, y-99).
        # If TOP-RIGHT is in beam, then the whole square fits (assuming convexity and proper angles).
        # But wait, checking top-right at y-99 means we need to have calculated/checked y-99.
        
        # Better:
        # Iterate y. Get x_start.
        # Check if (x_start + 99, y - 99) is in beam.
        # (x_start, y) is in beam (we just found it).
        # (x_start, y-99) is in beam (it should be if beam is somewhat straight, but check).
        # Actually, x_start increases with y. So x_start(y-99) <= x_start(y).
        # So (x_start(y), y-99) might be outside to the right? No, typically outside to the left unless beam is very wide vertical.
        
        # Tractor beam is usually y approx k*x.
        
        # Let's trace beam:
        # x start of beam at y.
        # Check if point (x + 99, y - 99) is in beam.
        # If yes, then we found a square of size 100x100.
        # The top-left corner is (x, y-99).
        
        # Note: (x+99, y-99) validity check requires y >= 99.
        
        if check_point(program, x + 99, y - 99) == 1:
            # Found it!
            return x * 10000 + (y - 99)
            
        y += 1

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(program))
    print("Part 2:", solve_part2(program))


import sys
import os
from collections import deque, defaultdict

class IntcodeComputer:
    def __init__(self, program, name="Amp"):
        self.memory = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        self.pc = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = deque()
        self.halted = False
        self.name = name
        self.waiting_for_input = False

    def get_addr(self, pos, mode):
        if mode == 0: # Position
            return self.memory[pos]
        elif mode == 1: # Immediate
            return pos
        elif mode == 2: # Relative
            return self.memory[pos] + self.relative_base
        else:
            raise ValueError(f"Unknown mode {mode}")

    def get_val(self, pos, mode):
        return self.memory[self.get_addr(pos, mode)]

    def set_val(self, pos, mode, val):
        self.memory[self.get_addr(pos, mode)] = val

    def add_input(self, val):
        self.inputs.append(val)
        self.waiting_for_input = False

    def get_output(self):
        if self.outputs:
            return self.outputs.popleft()
        return None
    
    def has_output(self):
        return len(self.outputs) > 0

    def run(self):
        # Run until halt or waiting for input
        while True:
            instr = self.memory[self.pc]
            opcode = instr % 100
            modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

            if opcode == 99:
                self.halted = True
                return

            elif opcode == 1: # Add
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], v1 + v2)
                self.pc += 4

            elif opcode == 2: # Mul
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                self.set_val(self.pc + 3, modes[2], v1 * v2)
                self.pc += 4

            elif opcode == 3: # Input
                if not self.inputs:
                    self.waiting_for_input = True
                    return # Wait for input
                
                val = self.inputs.popleft()
                self.set_val(self.pc + 1, modes[0], val)
                self.pc += 2

            elif opcode == 4: # Output
                v1 = self.get_val(self.pc + 1, modes[0])
                self.outputs.append(v1)
                self.pc += 2
                
            elif opcode == 5: # jump-if-true
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                if v1 != 0:
                    self.pc = v2
                else:
                    self.pc += 3

            elif opcode == 6: # jump-if-false
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                if v1 == 0:
                    self.pc = v2
                else:
                    self.pc += 3

            elif opcode == 7: # less-than
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                if v1 < v2:
                    self.set_val(self.pc + 3, modes[2], 1)
                else:
                    self.set_val(self.pc + 3, modes[2], 0)
                self.pc += 4

            elif opcode == 8: # equals
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                if v1 == v2:
                    self.set_val(self.pc + 3, modes[2], 1)
                else:
                    self.set_val(self.pc + 3, modes[2], 0)
                self.pc += 4
                
            elif opcode == 9: # adjust relative base
                v1 = self.get_val(self.pc + 1, modes[0])
                self.relative_base += v1
                self.pc += 2
            
            else:
                raise ValueError(f"Unknown opcode {opcode} at {self.pc} in {self.name}")

def solve_part1(program):
    computer = IntcodeComputer(program)
    computer.add_input(1) # Test mode
    computer.run()
    return computer.outputs[-1] # Keycode is the last output

def solve_part2(program):
    computer = IntcodeComputer(program)
    computer.add_input(2) # Sensor boost mode
    computer.run()
    return computer.outputs[-1]

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(program))
    print("Part 2:", solve_part2(program)) # Assuming standard Part 2 structure for Intcode days

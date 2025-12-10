
import sys
import os
import itertools
from collections import deque

class IntcodeComputer:
    def __init__(self, program, name="Amp"):
        self.memory = list(program)
        self.pc = 0
        self.inputs = deque()
        self.outputs = deque()
        self.halted = False
        self.name = name

    def get_val(self, pos, mode):
        # Support only Position (0) and Immediate (1) for now
        if mode == 0:
            # Address at pos
            addr = self.memory[pos]
            return self.memory[addr]
        elif mode == 1:
            return self.memory[pos]
        else:
            raise ValueError(f"Unknown mode {mode}")

    def add_input(self, val):
        self.inputs.append(val)

    def get_output(self):
        if self.outputs:
            return self.outputs.popleft()
        return None
    
    def has_output(self):
        return len(self.outputs) > 0

    def run(self):
        # Run until halt or waiting for input
        while True:
            if self.pc >= len(self.memory):
                self.halted = True
                return

            instr = self.memory[self.pc]
            opcode = instr % 100
            modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

            if opcode == 99:
                self.halted = True
                return

            elif opcode == 1: # Add
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                dest = self.memory[self.pc + 3]
                self.memory[dest] = v1 + v2
                self.pc += 4

            elif opcode == 2: # Mul
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                dest = self.memory[self.pc + 3]
                self.memory[dest] = v1 * v2
                self.pc += 4

            elif opcode == 3: # Input
                if not self.inputs:
                    return # Wait for input
                
                val = self.inputs.popleft()
                dest = self.memory[self.pc + 1]
                self.memory[dest] = val
                self.pc += 2

            elif opcode == 4: # Output
                v1 = self.get_val(self.pc + 1, modes[0])
                self.outputs.append(v1)
                self.pc += 2
                # We could return here to yield output immediately, or keep running
                # Usually better to keep running until input need or halt
                
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
                dest = self.memory[self.pc + 3]
                if v1 < v2:
                    self.memory[dest] = 1
                else:
                    self.memory[dest] = 0
                self.pc += 4

            elif opcode == 8: # equals
                v1 = self.get_val(self.pc + 1, modes[0])
                v2 = self.get_val(self.pc + 2, modes[1])
                dest = self.memory[self.pc + 3]
                if v1 == v2:
                    self.memory[dest] = 1
                else:
                    self.memory[dest] = 0
                self.pc += 4
            
            else:
                raise ValueError(f"Unknown opcode {opcode} at {self.pc} in {self.name}")

def solve_part1(program):
    max_signal = 0
    
    # Try every permutation of phase settings 0-4
    for phase_settings in itertools.permutations(range(5)):
        current_signal = 0
        
        # 5 amplifiers
        for i in range(5):
            amp = IntcodeComputer(program, name=f"Amp{i}")
            amp.add_input(phase_settings[i])
            amp.add_input(current_signal)
            amp.run()
            
            # Should have exactly one output
            out = amp.get_output()
            if out is not None:
                current_signal = out
            else:
                print("Error: Amp did not produce output")
                break
        
        if current_signal > max_signal:
            max_signal = current_signal
            
    return max_signal

def solve_part2(program):
    max_signal = 0
    
    # Try every permutation of phase settings 5-9
    for phase_settings in itertools.permutations(range(5, 10)):
        amps = [IntcodeComputer(program, name=f"Amp{i}") for i in range(5)]
        
        # Initialize with phase settings
        for i in range(5):
            amps[i].add_input(phase_settings[i])
            
        # Initial input to Amp A
        amps[0].add_input(0)
        
        last_e_output = 0
        
        # Run until E halts
        while not amps[4].halted:
            for i in range(5):
                amps[i].run()
                
                # Pass all outputs to next amp
                while amps[i].has_output():
                    val = amps[i].get_output()
                    next_amp_idx = (i + 1) % 5
                    amps[next_amp_idx].add_input(val)
                    
                    if i == 4:
                        last_e_output = val
                        
        if last_e_output > max_signal:
            max_signal = last_e_output
            
    return max_signal

def part2(data):
    # This function kept for signature compatibility if needed, but we use solve_part2 directly
    return solve_part2(data)

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(program))
    print("Part 2:", solve_part2(program))

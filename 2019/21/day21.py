
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

def solve_part1(program):
    computer = IntcodeComputer(program)
    
    # Logic: Jump if there's a hole in A, B, or C, BUT only if D is ground.
    # If D is a hole, jumping is suicide.
    # So: (NOT A) OR (NOT B) OR (NOT C) AND D
    # Equivalent to: NOT (A AND B AND C) AND D
    
    # Registers:
    # T = Temp
    # J = Jump (result)
    # A, B, C, D = sensors (True if ground)
    
    # We want J = (!A | !B | !C) & D
    
    instructions = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""
    computer.add_ascii_input(instructions.strip() + "\n")
    computer.run()
    
    outputs = computer.get_all_outputs()
    if not outputs:
        return "No output"
        
    last_val = outputs[-1]
    if last_val > 127:
        return last_val
    else:
        print(''.join(chr(c) for c in outputs))
        return "Failed"

def solve_part2(program):
    # Part 2 usually unlocks RUN command which uses more sensors.
    # We need to read the prompt but assuming standard Springdroid problem.
    # Usually: A, B, C, D, E, F, G, H, I ...
    # Run uses RUN instead of WALK.
    
    # Let's verify standard extended sensors: E, F, G, H, I.
    # Extended jump logic for RUN.
    # A jump distance is 4.
    
    # We want to jump if there is a hole at A, B, or C.
    # AND we land securely at D.
    # AND after landing at D, we can proceed.
    # If we land at D, we need to be able to jump again or walk.
    # So either E is ground (walk) or H is ground (jump from D).
    # So condition: (!A | !B | !C) & D & (E | H)
    
    computer = IntcodeComputer(program)
    
    instructions = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
RUN
"""
    computer.add_ascii_input(instructions.strip() + "\n")
    computer.run()
    
    outputs = computer.get_all_outputs()
    if not outputs:
        return "No output"
        
    last_val = outputs[-1]
    if last_val > 127:
        return last_val
    else:
        print(''.join(chr(c) for c in outputs))
        return "Failed"

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(list(program)))
    print("Part 2:", solve_part2(list(program)))

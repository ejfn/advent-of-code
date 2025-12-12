
import sys
import os
import re

class CPU:
    def __init__(self, registers=None):
        self.regs = [0, 0, 0, 0] if registers is None else list(registers)

    def addr(self, a, b, c):
        self.regs[c] = self.regs[a] + self.regs[b]

    def addi(self, a, b, c):
        self.regs[c] = self.regs[a] + b

    def mulr(self, a, b, c):
        self.regs[c] = self.regs[a] * self.regs[b]

    def muli(self, a, b, c):
        self.regs[c] = self.regs[a] * b

    def banr(self, a, b, c):
        self.regs[c] = self.regs[a] & self.regs[b]

    def bani(self, a, b, c):
        self.regs[c] = self.regs[a] & b

    def borr(self, a, b, c):
        self.regs[c] = self.regs[a] | self.regs[b]

    def bori(self, a, b, c):
        self.regs[c] = self.regs[a] | b

    def setr(self, a, b, c):
        self.regs[c] = self.regs[a]

    def seti(self, a, b, c):
        self.regs[c] = a

    def gtir(self, a, b, c):
        self.regs[c] = 1 if a > self.regs[b] else 0

    def gtri(self, a, b, c):
        self.regs[c] = 1 if self.regs[a] > b else 0

    def gtrr(self, a, b, c):
        self.regs[c] = 1 if self.regs[a] > self.regs[b] else 0

    def eqir(self, a, b, c):
        self.regs[c] = 1 if a == self.regs[b] else 0

    def eqri(self, a, b, c):
        self.regs[c] = 1 if self.regs[a] == b else 0

    def eqrr(self, a, b, c):
        self.regs[c] = 1 if self.regs[a] == self.regs[b] else 0

    def execute(self, opcode_name, a, b, c):
        getattr(self, opcode_name)(a, b, c)

ALl_OPCODES = [
    'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
    'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
]

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Split into two parts: samples and program
    # Samples are separated by blank lines and look like:
    # Before: [3, 2, 1, 1]
    # 9 2 1 2
    # After:  [3, 2, 2, 1]
    
    # The part 1 input ends when there are three newlines or more? 
    # Or just when the pattern breaks.
    # Usually in AoC there's a double newline between blocks, but here we have
    # blocks of 3 lines separated by newlines.
    
    parts = content.split('\n\n\n')
    samples_part = parts[0]
    program_part = parts[1] if len(parts) > 1 else ""
    
    # If split didn't work well (e.g. maybe 4 newlines or mixed), try robust parsing
    if len(parts) < 2:
        # Fallback: scan line by line
        lines = content.splitlines()
        samples = []
        program = []
        i = 0
        while i < len(lines):
            if lines[i].startswith('Before:'):
                before = list(map(int, lines[i][9:-1].split(', ')))
                instruction = list(map(int, lines[i+1].split()))
                after = list(map(int, lines[i+2][9:-1].split(', ')))
                samples.append({'before': before, 'instr': instruction, 'after': after})
                i += 4 # Skip empty line
            elif lines[i].strip():
                program.append(list(map(int, lines[i].split())))
                i += 1
            else:
                i += 1
    else:
        # Parse samples
        samples = []
        lines = samples_part.splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('Before:'):
                before = list(map(int, lines[i][9:-1].split(', ')))
                instruction = list(map(int, lines[i+1].split()))
                after = list(map(int, lines[i+2][9:-1].split(', ')))
                samples.append({'before': before, 'instr': instruction, 'after': after})
                i += 4 
            else:
                i += 1
        
        # Parse program
        program = []
        for line in program_part.splitlines():
            if line.strip():
                program.append(list(map(int, line.split())))
                
    return samples, program

def solve_part1(samples):
    count = 0
    for sample in samples:
        behave_count = 0
        for opcode in ALl_OPCODES:
            cpu = CPU(sample['before'])
            cpu.execute(opcode, sample['instr'][1], sample['instr'][2], sample['instr'][3])
            if cpu.regs == sample['after']:
                behave_count += 1
        if behave_count >= 3:
            count += 1
    return count

def solve_part2(samples, program):
    # Determine opcode mapping
    possible_opcodes = {i: set(ALl_OPCODES) for i in range(16)}
    
    for sample in samples:
        op_num = sample['instr'][0]
        valid_ops = set()
        for opcode in ALl_OPCODES:
            cpu = CPU(sample['before'])
            cpu.execute(opcode, sample['instr'][1], sample['instr'][2], sample['instr'][3])
            if cpu.regs == sample['after']:
                valid_ops.add(opcode)
        
        possible_opcodes[op_num] &= valid_ops
        
    # Reduce possibilities
    mapping = {}
    while len(mapping) < 16:
        # Find one with only 1 possibility
        for i in range(16):
            if i in mapping: continue
            if len(possible_opcodes[i]) == 1:
                op_name = list(possible_opcodes[i])[0]
                mapping[i] = op_name
                # Remove from others
                for j in range(16):
                    if j != i:
                        possible_opcodes[j].discard(op_name)
    
    # Run program
    cpu = CPU([0, 0, 0, 0])
    for instr in program:
        op_name = mapping[instr[0]]
        cpu.execute(op_name, instr[1], instr[2], instr[3])
        
    return cpu.regs[0]

def part1(filename):
    samples, _ = parse_input(filename)
    return solve_part1(samples)

def part2(filename):
    samples, program = parse_input(filename)
    return solve_part2(samples, program)

def run_example():
    # Example from description
    # Before: [3, 2, 1, 1]
    # 9 2 1 2
    # After:  [3, 2, 2, 1]
    sample = {
        'before': [3, 2, 1, 1],
        'instr': [9, 2, 1, 2],
        'after': [3, 2, 2, 1]
    }
    
    # Check matching opcodes
    cpu = CPU([3, 2, 1, 1])
    matches = []
    for op in ALl_OPCODES:
        cpu.regs = list(sample['before'])
        cpu.execute(op, 2, 1, 2)
        if cpu.regs == sample['after']:
            matches.append(op)
            
    print(f"Matches for example: {matches}")
    # Description says: mulr, addi, seti matches.
    # My matches should include these.
    expected = {'mulr', 'addi', 'seti'}
    assert expected.issubset(set(matches))
    print("Example passed!")

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {part1(input_file)}")
    print(f"Part 2: {part2(input_file)}")

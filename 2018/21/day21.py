
import sys

# Reusing CPU class from Day 19
class CPU:
    def __init__(self, registers=None, ip_bind=None):
        self.regs = [0] * 6 if registers is None else list(registers)
        self.ip_bind = ip_bind
        self.ip = 0

    def execute_instruction(self, op, a, b, c):
        if op == 'addr': self.regs[c] = self.regs[a] + self.regs[b]
        elif op == 'addi': self.regs[c] = self.regs[a] + b
        elif op == 'mulr': self.regs[c] = self.regs[a] * self.regs[b]
        elif op == 'muli': self.regs[c] = self.regs[a] * b
        elif op == 'banr': self.regs[c] = self.regs[a] & self.regs[b]
        elif op == 'bani': self.regs[c] = self.regs[a] & b
        elif op == 'borr': self.regs[c] = self.regs[a] | self.regs[b]
        elif op == 'bori': self.regs[c] = self.regs[a] | b
        elif op == 'setr': self.regs[c] = self.regs[a]
        elif op == 'seti': self.regs[c] = a
        elif op == 'gtir': self.regs[c] = 1 if a > self.regs[b] else 0
        elif op == 'gtri': self.regs[c] = 1 if self.regs[a] > b else 0
        elif op == 'gtrr': self.regs[c] = 1 if self.regs[a] > self.regs[b] else 0
        elif op == 'eqir': self.regs[c] = 1 if a == self.regs[b] else 0
        elif op == 'eqri': self.regs[c] = 1 if self.regs[a] == b else 0
        elif op == 'eqrr': self.regs[c] = 1 if self.regs[a] == self.regs[b] else 0

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    ip_bind = None
    program = []
    
    start_idx = 0
    first_line = lines[0].strip()
    if first_line.startswith('#ip'):
        ip_bind = int(first_line.split()[1])
        start_idx = 1
        
    for line in lines[start_idx:]:
        parts = line.split()
        op = parts[0]
        a = int(parts[1])
        b = int(parts[2])
        c = int(parts[3])
        program.append((op, a, b, c))
        
    # Find the instruction that checks Reg 0 (assuming eqrr X 0 Y or eqrr 0 X Y)
    check_ip = -1
    for i, (op, a, b, c) in enumerate(program):
        if op == 'eqrr' and (a == 0 or b == 0):
            check_ip = i
            break
            
    return ip_bind, program, check_ip

def solve_part1(filename):
    ip_bind, program, check_ip = parse_input(filename)
    cpu = CPU(ip_bind=ip_bind)
    
    # We run until IP hits check_ip
    # The value in the OTHER register (not 0) is the answer
    # Because if we set Reg 0 to that value, eqrr returns 1, and program halts.
    
    # Identify which register is comparison
    op, a, b, c = program[check_ip]
    target_reg = a if b == 0 else b
    
    while 0 <= cpu.ip < len(program):
        if cpu.ip == check_ip:
            return cpu.regs[target_reg]
        
        if cpu.ip_bind is not None:
            cpu.regs[cpu.ip_bind] = cpu.ip
            
        op, a, b, c = program[cpu.ip]
        cpu.execute_instruction(op, a, b, c)
        
        if cpu.ip_bind is not None:
            cpu.ip = cpu.regs[cpu.ip_bind]
            
        cpu.ip += 1

def solve_part2(filename):
    # Optimized reverse-engineered solution from assembly
    R5 = 0
    seen = set()
    last = None
    
    while True:
        R4 = R5 | 65536
        R5 = 13284195
        
        while True:
            R3 = R4 & 255
            R5 = R5 + R3
            R5 = R5 & 16777215
            R5 = R5 * 65899
            R5 = R5 & 16777215
            
            if 256 > R4:
                # This is where the program checks eqrr 5 0 3
                # So R5 is the candidate.
                if R5 in seen:
                    return last
                seen.add(R5)
                last = R5
                break
                
            R4 = R4 // 256
        
if __name__ == '__main__':
    import os
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

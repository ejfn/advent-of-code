
import sys
import os

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

    def run(self, program, max_cycles=0):
        # program is list of (op, a, b, c)
        
        cycle = 0
        while 0 <= self.ip < len(program):
            if max_cycles > 0 and cycle >= max_cycles:
                return False # Not finished
            
            # Write IP to register
            if self.ip_bind is not None:
                self.regs[self.ip_bind] = self.ip
                
            op, a, b, c = program[self.ip]
            self.execute_instruction(op, a, b, c)
            
            # Read IP from register
            if self.ip_bind is not None:
                self.ip = self.regs[self.ip_bind]
                
            self.ip += 1
            cycle += 1
            
        return True # Halted

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    ip_bind = None
    program = []
    
    first_line = lines[0].strip()
    if first_line.startswith('#ip'):
        ip_bind = int(first_line.split()[1])
        start_idx = 1
    else:
        start_idx = 0
        
    for line in lines[start_idx:]:
        parts = line.split()
        op = parts[0]
        a = int(parts[1])
        b = int(parts[2])
        c = int(parts[3])
        program.append((op, a, b, c))
        
    return ip_bind, program

def sum_divisors(n):
    total = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i*i != n:
                total += n // i
    return total

def get_part2_target(filename):
    ip_bind, program = parse_input(filename)
    cpu = CPU(registers=[1, 0, 0, 0, 0, 0], ip_bind=ip_bind)
    
    # Run slightly more than needed to initialize
    # The initialization takes some cycles
    # We stop when IP=1
    
    for _ in range(200):
        if cpu.ip == 1:
            # Check if this is the first time reaching the loop after init
            # Reg 1 should be large.
            if cpu.regs[1] > 1000:
                return cpu.regs[1]
        
        if cpu.ip_bind is not None:
            cpu.regs[cpu.ip_bind] = cpu.ip
            
        op, a, b, c = program[cpu.ip]
        cpu.execute_instruction(op, a, b, c)
        
        if cpu.ip_bind is not None:
            cpu.ip = cpu.regs[cpu.ip_bind]
            
        cpu.ip += 1
        
    return 0

def solve_part1(filename):
    ip_bind, program = parse_input(filename)
    cpu = CPU(ip_bind=ip_bind)
    cpu.run(program)
    return cpu.regs[0]

def solve_part2(filename):
    target = get_part2_target(filename)
    return sum_divisors(target)

def run_example():
    ex = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(ex)
        tmp_name = tmp.name
        
    p1 = solve_part1(tmp_name)
    assert p1 == 6
    print("Example passed!")
    os.remove(tmp_name)

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

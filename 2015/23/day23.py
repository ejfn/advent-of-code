import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def run(instructions, initial_a=0):
    regs = {'a': initial_a, 'b': 0}
    pc = 0
    
    while 0 <= pc < len(instructions):
        instr = instructions[pc]
        parts = instr.replace(',', '').split()
        op = parts[0]
        
        if op == 'hlf':
            regs[parts[1]] //= 2
            pc += 1
        elif op == 'tpl':
            regs[parts[1]] *= 3
            pc += 1
        elif op == 'inc':
            regs[parts[1]] += 1
            pc += 1
        elif op == 'jmp':
            pc += int(parts[1])
        elif op == 'jie':
            if regs[parts[1]] % 2 == 0:
                pc += int(parts[2])
            else:
                pc += 1
        elif op == 'jio':
            if regs[parts[1]] == 1:
                pc += int(parts[2])
            else:
                pc += 1
    
    return regs['b']

def part1(instructions):
    return run(instructions, initial_a=0)

def part2(instructions):
    return run(instructions, initial_a=1)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

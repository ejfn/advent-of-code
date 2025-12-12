import sys
import os

def get_val(x, regs):
    try:
        return int(x)
    except ValueError:
        return regs[x]

def run(instructions, regs):
    program = []
    # Parse instructions
    for line in instructions:
        parts = line.split()
        program.append(parts)
        
    pc = 0
    prog_len = len(program)
    
    while 0 <= pc < prog_len:
        parts = program[pc]
        op = parts[0]
        
        if op == 'cpy':
            x, y = parts[1], parts[2]
            if y in regs: # y must be a register
                regs[y] = get_val(x, regs)
        elif op == 'inc':
            x = parts[1]
            if x in regs:
                regs[x] += 1
        elif op == 'dec':
            x = parts[1]
            if x in regs:
                regs[x] -= 1
        elif op == 'jnz':
            x, y = parts[1], parts[2]
            val_x = get_val(x, regs)
            if val_x != 0:
                pc += get_val(y, regs)
                continue
        
        pc += 1
        
    return regs['a']

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        
    regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    return run(lines, regs)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        
    regs = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    return run(lines, regs)

def run_example():
    lines = [
        "cpy 41 a",
        "inc a",
        "inc a",
        "dec a",
        "jnz a 2",
        "dec a"
    ]
    regs = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    val = run(lines, regs)
    print(f"Example result: {val} (expected 42)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

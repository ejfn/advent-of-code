import sys
import os

def parse_val(x, regs):
    try:
        return int(x)
    except ValueError:
        return regs.get(x, 0)

def toggle(inst):
    # tgl x
    # one-arg: inc -> dec, others -> inc
    # two-arg: jnz -> cpy, others -> jnz
    op = inst[0]
    args = inst[1:]
    
    if len(args) == 1:
        if op == 'inc':
            return ['dec'] + args
        else:
            return ['inc'] + args
    elif len(args) == 2:
        if op == 'jnz':
            return ['cpy'] + args
        else:
            return ['jnz'] + args
    return inst

def run(instructions, initial_a=7):
    regs = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    # Make a copy of instructions as they will be modified
    code = [list(i) for i in instructions]
    pc = 0
    
    while 0 <= pc < len(code):
        # Optimization: Check for multiplication loop pattern
        # cpy b c
        # inc a
        # dec c
        # jnz c -2
        # dec d
        # jnz d -5
        if pc + 5 < len(code):
            i0 = code[pc]
            i1 = code[pc+1]
            i2 = code[pc+2]
            i3 = code[pc+3]
            i4 = code[pc+4]
            i5 = code[pc+5]
            
            # Check for specific structure in user input (lines 5-10)
            # 5: cpy b c
            # 6: inc a
            # 7: dec c
            # 8: jnz c -2
            # 9: dec d
            # 10: jnz d -5
            if (i0[0] == 'cpy' and i0[2] == 'c' and
                i1[0] == 'inc' and i1[1] == 'a' and
                i2[0] == 'dec' and i2[1] == 'c' and
                i3[0] == 'jnz' and i3[1] == 'c' and i3[2] == '-2' and
                i4[0] == 'dec' and i4[1] == 'd' and
                i5[0] == 'jnz' and i5[1] == 'd' and i5[2] == '-5'):
                
                # Perform multiplication: a += b * d
                # c = 0, d = 0
                val_b = parse_val(i0[1], regs)
                val_d = parse_val('d', regs) # current d
                
                regs['a'] += val_b * val_d
                regs['c'] = 0
                regs['d'] = 0
                pc += 6
                continue

        inst = code[pc]
        op = inst[0]
        
        if op == 'cpy':
            x, y = inst[1], inst[2]
            if y in regs: # y must be a register
                regs[y] = parse_val(x, regs)
        elif op == 'inc':
            x = inst[1]
            if x in regs:
                regs[x] += 1
        elif op == 'dec':
            x = inst[1]
            if x in regs:
                regs[x] -= 1
        elif op == 'jnz':
            x, y = inst[1], inst[2]
            val_x = parse_val(x, regs)
            val_y = parse_val(y, regs)
            if val_x != 0:
                pc += val_y
                continue
        elif op == 'tgl':
            x = inst[1]
            offset = parse_val(x, regs)
            target_idx = pc + offset
            if 0 <= target_idx < len(code):
                code[target_idx] = toggle(code[target_idx])
        
        pc += 1
        
    return regs['a']

def parse_input(lines):
    instructions = []
    for line in lines:
        if not line.strip(): continue
        parts = line.strip().split()
        instructions.append(parts)
    return instructions

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    instructions = parse_input(lines)
    return run(instructions, 7)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    instructions = parse_input(lines)
    return run(instructions, 12)

def run_example():
    # Example from problem
    raw = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
    """
    instructions = parse_input(raw.strip().split('\n'))
    # "In this example, the final value in register a is 3."
    # Initial regs assumed 0 unless set. My run function defaults to a=Input.
    # Here example starts empty regs mostly?
    # "cpy 2 a initializes register a to 2."
    # So initial register state doesn't matter much if it's overwritten first thing.
    # But run() takes initial_a. I should pass 0 or 7? Example says nothing about input value 7, 
    # it puts 7 in 'a' for the REAL puzzle.
    # For example, let's run with 0 (default).
    
    # Wait, run function signature is run(instructions, initial_a=7).
    # I should start with 0 for this example logic to hold?
    # "The rest of the electronics seem to place the keypad entry... in register a"
    # The example code sets 'a' immediately: `cpy 2 a`.
    # So initial `a` is overwritten.
    
    res = run(instructions, 0)
    print(f"Example result: {res} (Expected 3)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

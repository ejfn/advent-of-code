import sys
import os

def check_outputs(instructions, initial_a, limit=50):
    regs = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    outputs = []
    
    # Simple interpreter (no optimize needed for just generating output logic)
    # But we need 'out' support.
    
    while 0 <= pc < len(instructions) and len(outputs) < limit:
        inst = instructions[pc]
        op = inst[0]
        
        if op == 'cpy':
            x, y = inst[1], inst[2]
            val = int(x) if (isinstance(x, int) or x.lstrip('-').isdigit()) else regs[x]
            if y in regs: regs[y] = val
        elif op == 'inc':
            x = inst[1]
            if x in regs: regs[x] += 1
        elif op == 'dec':
            x = inst[1]
            if x in regs: regs[x] -= 1
        elif op == 'jnz':
            x, y = inst[1], inst[2]
            val_x = int(x) if (isinstance(x, int) or x.lstrip('-').isdigit()) else regs[x]
            val_y = int(y) if (isinstance(y, int) or y.lstrip('-').isdigit()) else regs[y]
            if val_x != 0:
                pc += val_y
                continue
        elif op == 'out':
            x = inst[1]
            val = int(x) if (isinstance(x, int) or x.lstrip('-').isdigit()) else regs[x]
            outputs.append(val)
            # Verify immediately?
            expected = (len(outputs) - 1) % 2 == 0 # 0 for 1st (idx 0), 1 for 2nd
            expected_val = 0 if expected else 1
            if val != expected_val:
                return False
        
        pc += 1
        
    return True

def parse_input(lines):
    instructions = []
    for line in lines:
        if not line.strip(): continue
        parts = line.strip().split()
        instructions.append(parts)
    return instructions

def solve_math(instructions):
    # Extract constants from lines 2 and 3
    # cpy 4 c
    # cpy 643 b
    # (Checking expected lines 1, 2 in 0-indexed list)
    try:
        val1 = int(instructions[1][1])
        val2 = int(instructions[2][1])
        offset = val1 * val2
    except:
        print("Warning: Could not parse input structure perfectly, using fallback or default.")
        offset = 0 # Should fail
        if len(instructions) > 2:
            print(f"Instructions start: {instructions[:3]}")
    
    # We need X = offset + a such that X is 101010... in binary (2, 10, 42, 170...)
    # Generate sequence
    curr = 2 # '10' binary
    while curr <= offset:
        # Next in sequence ...101010 -> ...10101010
        # Formula: curr * 4 + 2
        # 2 -> 10 (2*4+2)
        # 10 -> 42 (10*4+2)
        curr = curr * 4 + 2
        
    return curr - offset

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    instructions = parse_input(lines)
    
    answer = solve_math(instructions)
    
    # Verify
    if check_outputs(instructions, answer):
        return answer
    else:
        print(f"Mathematical solution {answer} failed verification!")
        # Fallback to brute force?
        i = 0
        while True:
            if check_outputs(instructions, i):
                return i
            i += 1

def part2():
    return "Click the link to activate the antenna!"

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

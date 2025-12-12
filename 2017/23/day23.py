import os
import sys
from collections import defaultdict


def parse_instructions(text):
    """Parse program instructions."""
    return [line.split() for line in text.strip().split('\n') if line.strip()]


def get_value(regs, x):
    """Get value - either register or integer."""
    try:
        return int(x)
    except ValueError:
        return regs[x]


def part1(instructions):
    """Count how many times mul is invoked."""
    regs = defaultdict(int)
    ip = 0
    mul_count = 0
    
    while 0 <= ip < len(instructions):
        inst = instructions[ip]
        op = inst[0]
        
        if op == 'set':
            regs[inst[1]] = get_value(regs, inst[2])
        elif op == 'sub':
            regs[inst[1]] -= get_value(regs, inst[2])
        elif op == 'mul':
            regs[inst[1]] *= get_value(regs, inst[2])
            mul_count += 1
        elif op == 'jnz':
            if get_value(regs, inst[1]) != 0:
                ip += get_value(regs, inst[2])
                continue
        
        ip += 1
    
    return mul_count


def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def part2(instructions):
    """
    Analyze the program - it counts non-primes in a range.
    
    When a=1:
    - b = 84 * 100 + 100000 = 108400
    - c = b + 17000 = 125400
    - Loop from b to c in steps of 17
    - For each value, check if it has any factor (i.e., is not prime)
    - h counts how many are NOT prime
    """
    # Extract constants from the program
    b_init = int(instructions[0][2])  # set b 84
    b = b_init * 100 + 100000
    c = b + 17000
    step = 17
    
    h = 0
    for n in range(b, c + 1, step):
        if not is_prime(n):
            h += 1
    
    return h


if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        instructions = parse_instructions(f.read())
    
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")

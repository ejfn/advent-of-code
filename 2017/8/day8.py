import os
import sys
from collections import defaultdict


def evaluate_condition(registers, cond_reg, op, value):
    """Evaluate a condition like 'a > 1' or 'b == 5'."""
    reg_val = registers[cond_reg]
    if op == '>':
        return reg_val > value
    elif op == '<':
        return reg_val < value
    elif op == '>=':
        return reg_val >= value
    elif op == '<=':
        return reg_val <= value
    elif op == '==':
        return reg_val == value
    elif op == '!=':
        return reg_val != value
    return False


def solve(instructions):
    """Returns (max final value, max ever value)."""
    registers = defaultdict(int)
    max_ever = 0
    
    for line in instructions:
        # Parse: reg inc/dec amount if cond_reg op value
        parts = line.split()
        reg = parts[0]
        action = parts[1]  # inc or dec
        amount = int(parts[2])
        # parts[3] is 'if'
        cond_reg = parts[4]
        op = parts[5]
        cond_val = int(parts[6])
        
        if evaluate_condition(registers, cond_reg, op, cond_val):
            if action == 'inc':
                registers[reg] += amount
            else:  # dec
                registers[reg] -= amount
            
            max_ever = max(max_ever, registers[reg])
    
    return max(registers.values()) if registers else 0, max_ever


def part1(instructions):
    return solve(instructions)[0]


def part2(instructions):
    return solve(instructions)[1]


def run_example():
    example = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
    instructions = example.strip().split('\n')
    assert part1(instructions) == 1
    print("Part 1 example passed!")
    assert part2(instructions) == 10
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        instructions = [line.strip() for line in f if line.strip()]
    
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")

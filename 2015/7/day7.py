import os
import sys
from functools import cache

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_circuit(instructions):
    wires = {}
    for line in instructions:
        parts = line.split(' -> ')
        dest = parts[1]
        expr = parts[0].split()
        wires[dest] = expr
    return wires

def solve(wires, override=None):
    cache_dict = {}
    
    def get_value(x):
        if x in cache_dict:
            return cache_dict[x]
        if x.isdigit() or (x[0] == '-' and x[1:].isdigit()):
            return int(x)
        if override and x in override:
            return override[x]
        
        expr = wires[x]
        if len(expr) == 1:
            # Direct assignment
            result = get_value(expr[0])
        elif len(expr) == 2:
            # NOT
            result = ~get_value(expr[1]) & 0xFFFF
        elif expr[1] == 'AND':
            result = get_value(expr[0]) & get_value(expr[2])
        elif expr[1] == 'OR':
            result = get_value(expr[0]) | get_value(expr[2])
        elif expr[1] == 'LSHIFT':
            result = (get_value(expr[0]) << int(expr[2])) & 0xFFFF
        elif expr[1] == 'RSHIFT':
            result = get_value(expr[0]) >> int(expr[2])
        else:
            raise ValueError(f"Unknown expression: {expr}")
        
        cache_dict[x] = result
        return result
    
    return get_value('a')

def part1(instructions):
    wires = parse_circuit(instructions)
    return solve(wires)

def part2(instructions):
    wires = parse_circuit(instructions)
    a_value = solve(wires)
    return solve(wires, override={'b': a_value})

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

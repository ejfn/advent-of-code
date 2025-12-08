import os
import sys
import itertools
import random

def parse_input(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    initials = {}
    gates = {}
    for line in lines:
        if ' -> ' in line:
            parts = line.split()
            in1 = parts[0]
            op = parts[1]
            in2 = parts[2]
            out = parts[4]
            gates[out] = (op, in1, in2)
        else:
            wire, val = line.split(': ')
            initials[wire] = int(val)
    return initials, gates

def get_value(wire, initials, gates, memo):
    if wire in initials:
        return initials[wire]
    if wire in memo:
        return memo[wire]
    op, in1, in2 = gates[wire]
    v1 = get_value(in1, initials, gates, memo)
    v2 = get_value(in2, initials, gates, memo)
    if op == 'AND':
        val = v1 & v2
    elif op == 'OR':
        val = v1 | v2
    elif op == 'XOR':
        val = v1 ^ v2
    else:
        raise ValueError(f"Unknown op {op}")
    memo[wire] = val
    return val

def get_affecting_gates(target_wires, gates, initials):
    affecting = set()
    stack = list(target_wires)
    visited = set()
    while stack:
        w = stack.pop()
        if w in visited:
            continue
        visited.add(w)
        if w in initials:
            continue
        if w in gates:
            op, in1, in2 = gates[w]
            affecting.add(w)
            stack.append(in1)
            stack.append(in2)
    return affecting

def simulate_with_swaps(initials, gates, z_wires, swap_pairs):
    driver = {w: gates[w] for w in gates}
    for a, b in swap_pairs:
        driver[a] = gates[b]
        driver[b] = gates[a]
    memo = {}
    z_values = {}
    for zw in z_wires:
        z_values[zw] = get_value(zw, initials, driver, memo)
    return z_values

def z_to_num(z_values, z_wires):
    num = 0
    for i, zw in enumerate(z_wires):
        num += z_values[zw] * (1 << i)
    return num

def part1(filename):
    initials, gates = parse_input(filename)
    x_wires = [f'x{i:02d}' for i in range(45)]
    y_wires = [f'y{i:02d}' for i in range(45)]
    x_num = 0
    for i, w in enumerate(x_wires):
        x_num += initials.get(w, 0) * (1 << i)
    y_num = 0
    for i, w in enumerate(y_wires):
        y_num += initials.get(w, 0) * (1 << i)
    expected = x_num + y_num
    print(f"x_num: {x_num}")
    print(f"y_num: {y_num}")
    print(f"expected: {expected}")
    print(f"Number of gates: {len(gates)}")
    memo = {}
    all_wires = set(initials.keys()) | set(gates.keys())
    z_wires = sorted([w for w in all_wires if w.startswith('z')], key=lambda w: int(w[1:]))
    print(f"Number of z wires: {len(z_wires)}")
    number = 0
    z_values = {}
    for i, zw in enumerate(z_wires):
        val = get_value(zw, initials, gates, memo)
        z_values[zw] = val
        if val:
            number += (1 << i)
    print(f"current: {number}")
    print(f"Expected popcount: {bin(expected).count('1')}")
    print(f"Current popcount: {bin(number).count('1')}")

    print("\nTest y=0:")
    initials_y0 = initials.copy()
    for w in y_wires:
        initials_y0[w] = 0
    memo_y0 = {}
    x_num_y0 = 0
    for i, w in enumerate(x_wires):
        x_num_y0 += initials_y0.get(w, 0) * (1 << i)
    z_num_y0 = 0
    for i, zw in enumerate(z_wires):
        val = get_value(zw, initials_y0, gates, memo_y0)
        if val:
            z_num_y0 += (1 << i)
    print(f"x_num_y0: {x_num_y0}")
    print(f"z_num_y0: {z_num_y0}")
    print("y=0 correct" if x_num_y0 == z_num_y0 else "y=0 broken")

    print("\nTest x=0:")
    initials_x0 = initials.copy()
    for w in x_wires:
        initials_x0[w] = 0
    memo_x0 = {}
    y_num_x0 = 0
    for i, w in enumerate(y_wires):
        y_num_x0 += initials_x0.get(w, 0) * (1 << i)
    z_num_x0 = 0
    for i, zw in enumerate(z_wires):
        val = get_value(zw, initials_x0, gates, memo_x0)
        if val:
            z_num_x0 += (1 << i)
    print(f"y_num_x0: {y_num_x0}")
    print(f"z_num_x0: {z_num_x0}")
    print("x=0 correct" if y_num_x0 == z_num_x0 else "x=0 broken")
    print("\nZ gates:")
    for zw in z_wires:
        op, in1, in2 = gates[zw]
        i_bit = int(zw[1:])
        print(f"z{i_bit:02d}: {in1} {op} {in2} -> {zw}")
    print("Differing bits:")
    differing_z = []
    for i in range(len(z_wires)):
        expected_bit = (expected >> i) & 1
        current_bit = z_values[z_wires[i]]
        if expected_bit != current_bit:
            print(f"  z{i:02d}: expected {expected_bit}, got {current_bit}")
            if z_wires[i] in gates:
                op, in1, in2 = gates[z_wires[i]]
                print(f"    Gate: {in1} {op} {in2} -> {z_wires[i]}")
            else:
                print(f"    Initial: {z_wires[i]}")
            differing_z.append(z_wires[i])
    affecting = get_affecting_gates(differing_z, gates, initials)
    print(f"\nNumber of affecting gates: {len(affecting)}")
    print("\nAffecting gates:")
    print(', '.join(sorted(affecting)))

    print("\nCluster affecting:")
    clusters = {
        '12-15': ['z12','z13','z14','z15'],
        '26-31': ['z26','z27','z28','z29','z30','z31'],
        '32-34': ['z32','z33','z34'],
        '36-39': ['z36','z37','z38','z39']
    }
    for name, cls in clusters.items():
        aff = get_affecting_gates(cls, gates, initials)
        print(f"{name}: {len(aff)}")

    return number

def part2(filename):
    # Part 2 not yet implemented; requires problem description
    return -1

if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), 'input.txt')
    print("Part 1:", part1(filename))
    print("Part 2:", part2(filename))

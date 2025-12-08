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

def get_value(wire, initials, gates, memo, visiting=None):
    if visiting is None:
        visiting = set()

    if wire in initials:
        return initials[wire]
    if wire in memo:
        return memo[wire]

    # Cycle detection
    if wire in visiting:
        return None  # Return None to signal a cycle

    if wire not in gates:
        return None

    visiting.add(wire)
    op, in1, in2 = gates[wire]
    v1 = get_value(in1, initials, gates, memo, visiting)
    v2 = get_value(in2, initials, gates, memo, visiting)
    visiting.remove(wire)

    if v1 is None or v2 is None:
        return None  # Propagate None for cycles

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
        z_values[zw] = get_value(zw, initials, driver, memo, visiting=None)
    return z_values, memo

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

def find_gate_by_signature(op, inputs, gates):
    """Find a gate that produces the given operation on the given inputs"""
    for out, (g_op, in1, in2) in gates.items():
        if g_op == op and {in1, in2} == set(inputs):
            return out
    return None

def get_z_dependencies(i, gates, initials):
    """Return what gates/wires should produce z_i"""
    x = f'x{i:02d}'
    y = f'y{i:02d}'

    if i == 0:
        # z00 = x00 XOR y00
        xor_out = find_gate_by_signature('XOR', [x, y], gates)
        and_out = find_gate_by_signature('AND', [x, y], gates)
        return {'z_out': xor_out, 'carry_out': and_out}
    else:
        # z_i = (x_i XOR y_i) XOR carry_{i-1}
        # carry_i = (x_i AND y_i) OR ((x_i XOR y_i) AND carry_{i-1})
        xor_xy = find_gate_by_signature('XOR', [x, y], gates)
        and_xy = find_gate_by_signature('AND', [x, y], gates)
        return {'xor_xy': xor_xy, 'and_xy': and_xy}

def validate_adder_structure(gates, initials):
    """Check which bits have the correct gate structure"""
    x_wires = [f'x{i:02d}' for i in range(45)]
    y_wires = [f'y{i:02d}' for i in range(45)]

    issues = []

    for i in range(45):
        x = f'x{i:02d}'
        y = f'y{i:02d}'
        z = f'z{i:02d}'

        if z not in gates:
            continue

        z_op, z_in1, z_in2 = gates[z]

        if i == 0:
            # z00 should be x00 XOR y00
            if z_op != 'XOR' or {z_in1, z_in2} != {x, y}:
                issues.append(f"z00 problem: {z_in1} {z_op} {z_in2} -> {z}")
        else:
            # z_i should be XOR of (x_i XOR y_i) and carry
            if z_op != 'XOR':
                issues.append(f"z{i:02d} is not XOR: {z_in1} {z_op} {z_in2} -> {z}")

    return issues

def find_gate_by_sig(op, inputs, gates):
    """Find gate output that produces op(inputs)"""
    for out, (g_op, in1, in2) in gates.items():
        if g_op == op and {in1, in2} == set(inputs):
            return out
    return None

def check_z_structure(bit, gates):
    """Check if z_{bit} has correct adder structure for that position"""
    z = f'z{bit:02d}'
    if z not in gates:
        return False, "z not found"

    op, in1, in2 = gates[z]
    x = f'x{bit:02d}'
    y = f'y{bit:02d}'

    if bit == 0:
        # z00 must be XOR(x00, y00)
        if op != 'XOR' or {in1, in2} != {x, y}:
            return False, "z00 not XOR(x00, y00)"
        return True, None
    else:
        # z_i must be XOR gate
        if op != 'XOR':
            return False, "z_i is not XOR"

        # One input should be x_i XOR y_i
        xor_xy = find_gate_by_sig('XOR', [x, y], gates)
        if xor_xy is None or xor_xy not in {in1, in2}:
            return False, "z_i inputs don't include x_i XOR y_i"

        return True, None

def part2(filename):
    initials, gates = parse_input(filename)

    # Find structural defects
    swapped = set()

    for out, (op, in1, in2) in gates.items():
        # Rule 1: z wires (except z45) must be XOR gates
        if out.startswith('z') and out != 'z45':
            if op != 'XOR':
                swapped.add(out)
                print(f"Rule 1: {out} is {op}, should be XOR")

        # Rule 2: XOR gates with x,y inputs should feed into another XOR (the z output)
        #         unless it's x00,y00 which directly produces z00
        if op == 'XOR':
            if (in1.startswith('x') or in1.startswith('y')) and (in2.startswith('x') or in2.startswith('y')):
                # This is x_i XOR y_i
                if in1 == 'x00' or in2 == 'x00':
                    # z00 = x00 XOR y00, this is fine
                    continue
                # This should feed into another XOR
                # Check if this gate's output goes to a XOR
                feeds_xor = False
                for other_out, (other_op, other_in1, other_in2) in gates.items():
                    if other_op == 'XOR' and (other_in1 == out or other_in2 == out):
                        feeds_xor = True
                        break
                if not feeds_xor:
                    swapped.add(out)
                    print(f"Rule 2: {out} = {in1} XOR {in2} doesn't feed XOR")

        # Rule 3: XOR gates that don't have x,y inputs should produce z outputs
        if op == 'XOR':
            has_xy = (in1.startswith('x') or in1.startswith('y') or
                     in2.startswith('x') or in2.startswith('y'))
            if not has_xy and not out.startswith('z'):
                swapped.add(out)
                print(f"Rule 3: {out} = {in1} XOR {in2} should produce z")

        # Rule 4: AND gates (except x00 AND y00) should feed into OR gates
        if op == 'AND':
            if (in1 == 'x00' and in2 == 'y00') or (in1 == 'y00' and in2 == 'x00'):
                continue  # x00 AND y00 is the initial carry
            feeds_or = False
            for other_out, (other_op, other_in1, other_in2) in gates.items():
                if other_op == 'OR' and (other_in1 == out or other_in2 == out):
                    feeds_or = True
                    break
            if not feeds_or:
                swapped.add(out)
                print(f"Rule 4: {out} = {in1} AND {in2} doesn't feed OR")

    print(f"\nSwapped wires found: {sorted(swapped)}")
    return ','.join(sorted(swapped))

if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), 'input.txt')
    print("Part 1:", part1(filename))
    print("Part 2:", part2(filename))

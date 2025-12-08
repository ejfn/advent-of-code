import os
import sys

def parse_input(filename):
    """Parse the input file to get registers and program."""
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    reg_a = int(lines[0].split(': ')[1])
    reg_b = int(lines[1].split(': ')[1])
    reg_c = int(lines[2].split(': ')[1])
    program = list(map(int, lines[4].split(': ')[1].split(',')))

    return reg_a, reg_b, reg_c, program

def get_combo_value(operand, reg_a, reg_b, reg_c):
    """Get the value of a combo operand."""
    if operand <= 3:
        return operand
    elif operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c
    else:
        raise ValueError(f"Invalid combo operand: {operand}")

def run_program(reg_a, reg_b, reg_c, program):
    """Run the program and return the output."""
    ip = 0  # instruction pointer
    output = []

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv
            combo = get_combo_value(operand, reg_a, reg_b, reg_c)
            reg_a = reg_a // (2 ** combo)
            ip += 2
        elif opcode == 1:  # bxl
            reg_b = reg_b ^ operand
            ip += 2
        elif opcode == 2:  # bst
            combo = get_combo_value(operand, reg_a, reg_b, reg_c)
            reg_b = combo % 8
            ip += 2
        elif opcode == 3:  # jnz
            if reg_a != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            reg_b = reg_b ^ reg_c
            ip += 2
        elif opcode == 5:  # out
            combo = get_combo_value(operand, reg_a, reg_b, reg_c)
            output.append(combo % 8)
            ip += 2
        elif opcode == 6:  # bdv
            combo = get_combo_value(operand, reg_a, reg_b, reg_c)
            reg_b = reg_a // (2 ** combo)
            ip += 2
        elif opcode == 7:  # cdv
            combo = get_combo_value(operand, reg_a, reg_b, reg_c)
            reg_c = reg_a // (2 ** combo)
            ip += 2

    return output

def run_example():
    """Test with the examples from the problem."""
    # Example: If register C contains 9, the program 2,6 would set register B to 1.
    output = run_program(0, 0, 9, [2, 6])
    print(f"Example 1 (should have B=1): output={output}")

    # Example: If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    output = run_program(10, 0, 0, [5, 0, 5, 1, 5, 4])
    print(f"Example 2 (should output 0,1,2): {','.join(map(str, output))}")

    # Example: If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    output = run_program(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    print(f"Example 3 (should output 4,2,5,6,7,7,7,7,3,1,0): {','.join(map(str, output))}")

    # Example: If register B contains 29, the program 1,7 would set register B to 26.
    output = run_program(0, 29, 0, [1, 7])
    print(f"Example 4 (should have B=26): output={output}")

    # Example: If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    output = run_program(0, 2024, 43690, [4, 0])
    print(f"Example 5 (should have B=44354): output={output}")

    # Main example from problem
    output = run_program(729, 0, 0, [0, 1, 5, 4, 3, 0])
    print(f"Main example (should output 4,6,3,5,6,3,5,2,1,0): {','.join(map(str, output))}")

def part1():
    """Solve part 1."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    reg_a, reg_b, reg_c, program = parse_input(input_file)

    print(f"Initial state: A={reg_a}, B={reg_b}, C={reg_c}")
    print(f"Program: {program}")

    output = run_program(reg_a, reg_b, reg_c, program)
    result = ','.join(map(str, output))
    print(f"Output: {result}")
    return result

def part2():
    """Solve part 2."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    reg_a, reg_b, reg_c, program = parse_input(input_file)

    # Part 2 implementation will go here
    return None

if __name__ == "__main__":
    print("=" * 50)
    print("Testing examples:")
    print("=" * 50)
    run_example()
    print()

    print("=" * 50)
    print("Part 1:")
    print("=" * 50)
    result1 = part1()
    print()

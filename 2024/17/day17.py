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
    """Solve part 2 - find the lowest A that makes the program output itself."""
    input_file = os.path.join(sys.path[0], 'input.txt')
    reg_a, reg_b, reg_c, program = parse_input(input_file)

    target = program
    print(f"Target output: {target}")
    print(f"Program length: {len(program)}")

    # The program processes A in a loop, dividing it by 8 each iteration (looking at opcode 0 with operand 3)
    # Each iteration outputs one value based on the lower bits of A
    # We need to work backwards: build A from the output we want

    # Strategy: Build A digit by digit in base 8 (octal)
    # Start from the end of the target output and work backwards

    def find_a_recursive(target_output, current_a=0, depth=0):
        """Recursively find A that produces the target output."""
        if depth == len(target_output):
            # Check if this A actually works
            output = run_program(current_a, 0, 0, program)
            if output == target_output:
                return current_a
            return None

        # We're building A from most significant to least significant
        # Try all possible 3-bit values (0-7) for this position
        for digit in range(8):
            candidate_a = (current_a << 3) | digit

            # Test if this candidate produces the correct output so far
            output = run_program(candidate_a, 0, 0, program)

            # Check if the output matches what we need
            # We're building from the end, so compare from the end
            expected_len = depth + 1
            if len(output) >= expected_len:
                # Check if the last 'expected_len' outputs match the last 'expected_len' of target
                if output[-expected_len:] == target_output[-expected_len:]:
                    result = find_a_recursive(target_output, candidate_a, depth + 1)
                    if result is not None:
                        return result

        return None

    # Try to find A starting from 0
    result = find_a_recursive(target)

    if result:
        # Verify the result
        output = run_program(result, 0, 0, program)
        print(f"Found A = {result}")
        print(f"Output: {output}")
        print(f"Target: {target}")
        print(f"Match: {output == target}")
        return result
    else:
        print("No solution found!")
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

    print("=" * 50)
    print("Part 2:")
    print("=" * 50)
    result2 = part2()
    print()

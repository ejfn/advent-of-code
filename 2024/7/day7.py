import os
import sys
from itertools import product

def parse_input(filename):
    """Parse the input file and return list of (test_value, numbers)"""
    equations = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            test_value, numbers_str = line.split(':')
            test_value = int(test_value)
            numbers = list(map(int, numbers_str.split()))
            equations.append((test_value, numbers))
    return equations

def evaluate_left_to_right(numbers, operators):
    """Evaluate expression left-to-right with given operators"""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result = result + numbers[i + 1]
        elif op == '*':
            result = result * numbers[i + 1]
        elif op == '||':
            # Concatenation: combine digits
            result = int(str(result) + str(numbers[i + 1]))
    return result

def can_produce_value(test_value, numbers):
    """Check if any combination of + and * can produce test_value"""
    if len(numbers) == 1:
        return numbers[0] == test_value

    # Number of operators needed is len(numbers) - 1
    num_operators = len(numbers) - 1

    # Try all combinations of + and *
    for operators in product(['+', '*'], repeat=num_operators):
        if evaluate_left_to_right(numbers, operators) == test_value:
            return True
    return False

def part1():
    """Solve part 1"""
    equations = parse_input(os.path.join(sys.path[0], 'input.txt'))

    total = 0
    for test_value, numbers in equations:
        if can_produce_value(test_value, numbers):
            total += test_value

    return total

def can_produce_value_with_concat(test_value, numbers):
    """Check if any combination of +, *, and || can produce test_value"""
    if len(numbers) == 1:
        return numbers[0] == test_value

    # Number of operators needed is len(numbers) - 1
    num_operators = len(numbers) - 1

    # Try all combinations of +, *, and ||
    for operators in product(['+', '*', '||'], repeat=num_operators):
        if evaluate_left_to_right(numbers, operators) == test_value:
            return True
    return False

def part2():
    """Solve part 2"""
    equations = parse_input(os.path.join(sys.path[0], 'input.txt'))

    total = 0
    for test_value, numbers in equations:
        if can_produce_value_with_concat(test_value, numbers):
            total += test_value

    return total

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

import os
import sys


def load_input():
    """Load input from input.txt in the script's directory."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        return f.read()


def parse_worksheet(worksheet):
    """
    Parse worksheet where problems are separated by completely blank vertical columns.
    Within each problem, each row gives one number, and the last row gives the operation.
    """
    lines = worksheet.strip().split('\n')
    if len(lines) < 4:
        return []

    # Remove row labels (1→, 2→, etc.)
    rows = []
    for line in lines:
        if '→' in line:
            rows.append(line.split('→', 1)[1])
        else:
            rows.append(line)

    # Pad all rows to same length
    max_len = max(len(row) for row in rows)
    padded_rows = [row.ljust(max_len) for row in rows]

    # Find problem boundaries by locating completely blank vertical columns
    problem_ranges = []
    in_problem = False
    start = 0

    for col in range(max_len):
        # Check if this column is completely blank across all rows
        is_blank = all(padded_rows[row][col] == ' ' for row in range(len(padded_rows)))

        if not is_blank and not in_problem:
            start = col
            in_problem = True
        elif is_blank and in_problem:
            problem_ranges.append((start, col))
            in_problem = False

    if in_problem:
        problem_ranges.append((start, max_len))

    # Parse each problem
    problems = []
    for start, end in problem_ranges:
        # Extract this problem's text from all rows
        problem_lines = [padded_rows[i][start:end].strip() for i in range(len(padded_rows))]

        # Last line is operations, preceding lines are numbers
        numbers = []
        for i in range(len(problem_lines) - 1):
            if problem_lines[i]:
                numbers.append(int(problem_lines[i]))

        # Extract operations from last line
        operations = []
        op_line = problem_lines[-1]
        for char in op_line:
            if char in ['+', '*']:
                operations.append(char)

        if numbers and operations:
            problems.append((numbers, operations))

    return problems


def evaluate_expression(numbers, operations):
    """
    Evaluate expression using the single operation between all numbers.
    The operation (+ or *) is applied between all consecutive numbers.
    """
    if not numbers:
        return 0
    if not operations:
        return numbers[0] if len(numbers) == 1 else 0

    result = numbers[0]
    op = operations[0]  # Single operation for all numbers

    for i in range(1, len(numbers)):
        if op == '+':
            result += numbers[i]
        elif op == '*':
            result *= numbers[i]

    return result


def part1():
    """
    Solve Part 1: Parse worksheet, evaluate expressions, sum results.
    """
    worksheet = load_input()
    problems = parse_worksheet(worksheet)

    # Debug: print first few problems
    # print(f"Total problems found: {len(problems)}")
    # for i, (numbers, operations) in enumerate(problems[:10]):
    #     result = evaluate_expression(numbers, operations)
    #     print(f"Problem {i}: {numbers} with ops {operations} = {result}")

    # Evaluate each problem and sum results
    total = 0
    for numbers, operations in problems:
        if numbers:
            result = evaluate_expression(numbers, operations)
            total += result

    return total


def parse_worksheet_part2(worksheet):
    """
    Parse worksheet for Part 2: read right-to-left, column by column.
    Each column within a problem gives one number (top-to-bottom digits).
    """
    lines = worksheet.strip().split('\n')
    if len(lines) < 4:
        return []

    # Remove row labels
    rows = []
    for line in lines:
        if '→' in line:
            rows.append(line.split('→', 1)[1])
        else:
            rows.append(line)

    # Pad all rows to same length
    max_len = max(len(row) for row in rows)
    padded_rows = [row.ljust(max_len) for row in rows]

    # Find problem boundaries (completely blank columns)
    problem_ranges = []
    in_problem = False
    start = 0

    for col in range(max_len):
        is_blank = all(padded_rows[row][col] == ' ' for row in range(len(padded_rows)))

        if not is_blank and not in_problem:
            start = col
            in_problem = True
        elif is_blank and in_problem:
            problem_ranges.append((start, col))
            in_problem = False

    if in_problem:
        problem_ranges.append((start, max_len))

    # Parse each problem right-to-left, column by column
    problems = []
    for start, end in problem_ranges:
        numbers = []

        # Read columns right-to-left within this problem
        for col in range(end - 1, start - 1, -1):
            # Read this column top-to-bottom (excluding operator row)
            digits = []
            for row in range(len(padded_rows) - 1):  # Exclude last row (operator)
                char = padded_rows[row][col]
                if char.isdigit():
                    digits.append(char)

            # If we got digits, form a number
            if digits:
                number = int(''.join(digits))
                numbers.append(number)

        # Get operation from last row
        operations = []
        for col in range(start, end):
            char = padded_rows[-1][col]
            if char in ['+', '*']:
                operations.append(char)
                break  # Only one operation per problem

        if numbers and operations:
            problems.append((numbers, operations))

    return problems


def part2():
    """
    Solve Part 2: Read worksheet right-to-left, column by column.
    """
    worksheet = load_input()
    problems = parse_worksheet_part2(worksheet)

    total = 0
    for numbers, operations in problems:
        if numbers:
            result = evaluate_expression(numbers, operations)
            total += result

    return total


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
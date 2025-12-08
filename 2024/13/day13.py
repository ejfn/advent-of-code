import os
import sys
import re


def parse_input(filename):
    """Parse the input file and return list of machines."""
    with open(filename, 'r') as f:
        content = f.read().strip()

    machines = []
    blocks = content.split('\n\n')

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) != 3:
            continue

        # Parse Button A: X+94, Y+34
        match_a = re.search(r'Button A: X\+(\d+), Y\+(\d+)', lines[0])
        # Parse Button B: X+22, Y+67
        match_b = re.search(r'Button B: X\+(\d+), Y\+(\d+)', lines[1])
        # Parse Prize: X=8400, Y=5400
        match_p = re.search(r'Prize: X=(\d+), Y=(\d+)', lines[2])

        if match_a and match_b and match_p:
            ax, ay = int(match_a.group(1)), int(match_a.group(2))
            bx, by = int(match_b.group(1)), int(match_b.group(2))
            px, py = int(match_p.group(1)), int(match_p.group(2))
            machines.append(((ax, ay), (bx, by), (px, py)))

    return machines


def solve_machine(machine, max_presses=100):
    """
    Solve for minimum tokens to win prize on a machine.
    Returns cost if winnable, None otherwise.

    We need to solve:
    a * ax + b * bx = px
    a * ay + b * by = py

    Where a, b are non-negative integers <= max_presses
    Cost is 3*a + 1*b
    """
    (ax, ay), (bx, by), (px, py) = machine

    # Using Cramer's rule to solve the system
    # a * ax + b * bx = px
    # a * ay + b * by = py

    det = ax * by - ay * bx

    if det == 0:
        # No unique solution
        return None

    # Solve for a and b
    a_num = px * by - py * bx
    b_num = ax * py - ay * px

    # Check if we get integer solutions
    if a_num % det != 0 or b_num % det != 0:
        return None

    a = a_num // det
    b = b_num // det

    # Check constraints
    if a < 0 or b < 0:
        return None

    if max_presses is not None and (a > max_presses or b > max_presses):
        return None

    # Verify solution
    if a * ax + b * bx == px and a * ay + b * by == py:
        return 3 * a + b

    return None


def part1():
    """Solve part 1 of the puzzle."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    machines = parse_input(input_path)

    total_cost = 0
    prizes_won = 0

    for machine in machines:
        cost = solve_machine(machine, max_presses=100)
        if cost is not None:
            total_cost += cost
            prizes_won += 1

    return total_cost


def part2():
    """Solve part 2 of the puzzle."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    machines = parse_input(input_path)

    # Part 2: Add 10000000000000 to prize coordinates
    offset = 10000000000000
    adjusted_machines = []
    for (ax, ay), (bx, by), (px, py) in machines:
        adjusted_machines.append(((ax, ay), (bx, by), (px + offset, py + offset)))

    total_cost = 0
    prizes_won = 0

    for machine in adjusted_machines:
        cost = solve_machine(machine, max_presses=None)
        if cost is not None:
            total_cost += cost
            prizes_won += 1

    return total_cost


def run_example():
    """Test with the example from the puzzle."""
    example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    # Save to temp file
    with open('/tmp/example.txt', 'w') as f:
        f.write(example)

    machines = parse_input('/tmp/example.txt')
    print(f"Parsed {len(machines)} machines")

    for i, machine in enumerate(machines):
        (ax, ay), (bx, by), (px, py) = machine
        print(f"\nMachine {i+1}:")
        print(f"  Button A: X+{ax}, Y+{ay}")
        print(f"  Button B: X+{bx}, Y+{by}")
        print(f"  Prize: X={px}, Y={py}")

        cost = solve_machine(machine, max_presses=100)
        if cost is not None:
            print(f"  → Winnable with cost {cost}")
        else:
            print(f"  → Not winnable")

    # Calculate total
    total = 0
    for machine in machines:
        cost = solve_machine(machine, max_presses=100)
        if cost is not None:
            total += cost

    print(f"\nTotal minimum tokens: {total}")
    print(f"Expected: 480")


if __name__ == "__main__":
    print("Testing with example:")
    run_example()

    print("\n" + "="*50)
    print("Part 1:")
    result1 = part1()
    print(result1)

    print("\nPart 2:")
    result2 = part2()
    print(result2)

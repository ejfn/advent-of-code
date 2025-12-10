import os
import sys
import re

def parse_line(line):
    """Parse a line to extract target state, buttons, and joltage (ignored)."""
    # Extract the indicator diagram [...]
    diagram_match = re.search(r'\[([.#]+)\]', line)
    if not diagram_match:
        return None

    diagram = diagram_match.group(1)
    target = [1 if c == '#' else 0 for c in diagram]
    n_lights = len(target)

    # Extract button configurations (...)
    buttons = []
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    for match in button_matches:
        indices = [int(x) for x in match.split(',')]
        buttons.append(indices)

    return target, buttons, n_lights

def solve_gf2(target, buttons, n_lights):
    """
    Solve the system of linear equations over GF(2).
    We want to find x such that Ax = b (mod 2), where:
    - A is the matrix where A[i][j] = 1 if button j toggles light i
    - x is the number of times each button is pressed (mod 2)
    - b is the target state

    Returns the minimum number of button presses (sum of x values).
    """
    n_buttons = len(buttons)

    # Build the matrix A where A[light][button] = 1 if button toggles light
    A = [[0] * n_buttons for _ in range(n_lights)]
    for btn_idx, btn in enumerate(buttons):
        for light in btn:
            A[light][btn_idx] = 1

    # Augmented matrix [A | b]
    aug = [A[i][:] + [target[i]] for i in range(n_lights)]

    # Gaussian elimination over GF(2)
    pivot_col = []
    row = 0
    for col in range(n_buttons):
        # Find pivot
        pivot_row = None
        for r in range(row, n_lights):
            if aug[r][col] == 1:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        # Swap rows
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_col.append(col)

        # Eliminate
        for r in range(n_lights):
            if r != row and aug[r][col] == 1:
                for c in range(n_buttons + 1):
                    aug[r][c] ^= aug[row][c]

        row += 1

    # Check for inconsistency
    for r in range(row, n_lights):
        if aug[r][n_buttons] == 1:
            return None  # No solution

    # Back-substitution to find solution with minimum button presses
    # We have free variables, so we need to find the solution with min sum
    free_vars = []
    for col in range(n_buttons):
        if col not in pivot_col:
            free_vars.append(col)

    if not free_vars:
        # Unique solution
        solution = [0] * n_buttons
        for r, col in enumerate(pivot_col):
            solution[col] = aug[r][n_buttons]
        return sum(solution)

    # Try all combinations of free variables
    min_presses = float('inf')
    for mask in range(1 << len(free_vars)):
        solution = [0] * n_buttons

        # Set free variables
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1

        # Compute dependent variables
        for r in range(len(pivot_col)):
            col = pivot_col[r]
            val = aug[r][n_buttons]
            for c in range(n_buttons):
                if c != col:
                    val ^= (aug[r][c] * solution[c])
            solution[col] = val

        # Verify solution
        valid = True
        for light in range(n_lights):
            state = 0
            for btn_idx, btn in enumerate(buttons):
                if solution[btn_idx] == 1 and light in btn:
                    state ^= 1
            if state != target[light]:
                valid = False
                break

        if valid:
            min_presses = min(min_presses, sum(solution))

    return min_presses if min_presses != float('inf') else None

def part1():
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0
    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            continue

        target, buttons, n_lights = parsed
        min_presses = solve_gf2(target, buttons, n_lights)
        if min_presses is not None:
            total += min_presses

    return total

def part2():
    # Part 2 will be revealed after Part 1
    return 0

def run_example():
    """Test with the example from the puzzle."""
    examples = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]

    expected = [2, 3, 2]

    for i, line in enumerate(examples):
        parsed = parse_line(line)
        if parsed is None:
            print(f"Example {i+1}: Failed to parse")
            continue

        target, buttons, n_lights = parsed
        print(f"Example {i+1}: {n_lights} lights, {len(buttons)} buttons")
        print(f"  Target: {target}")
        print(f"  Buttons: {buttons}")

        min_presses = solve_gf2(target, buttons, n_lights)
        print(f"  Result: {min_presses} (expected {expected[i]})")
        print()

if __name__ == "__main__":
    print("=== Testing Examples ===")
    run_example()

    print("\n=== Part 1 ===")
    print(part1())

    print("\n=== Part 2 ===")
    print(part2())

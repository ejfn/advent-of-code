import os
import sys


# Part 1 keypad
KEYPAD1 = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']
]

# Part 2 diamond keypad
KEYPAD2 = [
    [None, None, '1', None, None],
    [None, '2', '3', '4', None],
    ['5', '6', '7', '8', '9'],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None]
]

MOVES = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}


def solve(instructions, keypad, start_r, start_c):
    """Find bathroom code by following instructions on keypad."""
    rows = len(keypad)
    cols = len(keypad[0])
    r, c = start_r, start_c
    code = []
    
    for line in instructions:
        for move in line:
            dr, dc = MOVES[move]
            nr, nc = r + dr, c + dc
            
            # Check bounds and valid key
            if 0 <= nr < rows and 0 <= nc < cols and keypad[nr][nc] is not None:
                r, c = nr, nc
        
        code.append(keypad[r][c])
    
    return ''.join(code)


def part1(instructions):
    return solve(instructions, KEYPAD1, 1, 1)  # Start at '5'


def part2(instructions):
    return solve(instructions, KEYPAD2, 2, 0)  # Start at '5'


def run_example():
    example = ["ULL", "RRDDD", "LURDL", "UUUUD"]
    assert part1(example) == "1985"
    print("Part 1 example passed!")
    
    assert part2(example) == "5DB3"
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        instructions = [line.strip() for line in f if line.strip()]
    
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")

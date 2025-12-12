import sys
import os
import re
import math

def parse_input(lines):
    discs = []
    # Disc #1 has 17 positions; at time=0, it is at position 15.
    pattern = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.')
    
    for line in lines:
        match = pattern.search(line)
        if match:
            disc_num = int(match.group(1))
            positions = int(match.group(2))
            start_pos = int(match.group(3))
            discs.append((positions, start_pos, disc_num))
    return discs

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def solve(discs):
    time = 0
    step = 1
    
    for positions, start_pos, disc_num in discs:
        # Condition: (start_pos + time + disc_num) % positions == 0
        while (start_pos + time + disc_num) % positions != 0:
            time += step
        
        # Once satisfied, we must maintain this condition.
        # The period of validity is 'positions'.
        # The combined period is LCM(current_step, positions).
        step = lcm(step, positions)
        
    return time

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    discs = parse_input(lines)
    return solve(discs)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    discs = parse_input(lines)
    # Part 2: Add a new disc
    # a new disc with 11 positions and starting at position 0 has appeared 
    # exactly one second below the previously-bottom disc.
    next_disc_num = len(discs) + 1
    discs.append((11, 0, next_disc_num))
    
    return solve(discs)

def run_example():
    lines = [
        "Disc #1 has 5 positions; at time=0, it is at position 4.",
        "Disc #2 has 2 positions; at time=0, it is at position 1."
    ]
    discs = parse_input(lines)
    result = solve(discs)
    print(f"Example result: {result} (expected 5)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

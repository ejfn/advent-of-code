import os
import sys


def parse_input(text):
    """Parse instructions like 'R2, L3' into list of (turn, steps)."""
    instructions = []
    for inst in text.strip().split(', '):
        turn = inst[0]
        steps = int(inst[1:])
        instructions.append((turn, steps))
    return instructions


# Directions: 0=N, 1=E, 2=S, 3=W
DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]


def part1(instructions):
    """Calculate Manhattan distance to final position."""
    x, y = 0, 0
    direction = 0  # Facing North
    
    for turn, steps in instructions:
        if turn == 'R':
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        
        x += DX[direction] * steps
        y += DY[direction] * steps
    
    return abs(x) + abs(y)


def part2(instructions):
    """Find first position visited twice."""
    x, y = 0, 0
    direction = 0
    visited = {(0, 0)}
    
    for turn, steps in instructions:
        if turn == 'R':
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        
        # Walk step by step to track all intermediate positions
        for _ in range(steps):
            x += DX[direction]
            y += DY[direction]
            
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))
    
    return None


def run_example():
    assert part1(parse_input("R2, L3")) == 5
    assert part1(parse_input("R2, R2, R2")) == 2
    assert part1(parse_input("R5, L5, R5, R3")) == 12
    print("Part 1 examples passed!")
    
    assert part2(parse_input("R8, R4, R4, R8")) == 4
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        instructions = parse_input(f.read())
    
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")

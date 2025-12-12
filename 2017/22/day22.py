import os
import sys


def parse_input(text):
    """Parse grid into set of infected positions."""
    lines = text.strip().split('\n')
    infected = set()
    
    mid_y = len(lines) // 2
    mid_x = len(lines[0]) // 2
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                infected.add((x - mid_x, mid_y - y))
    
    return infected


# Directions: 0=up, 1=right, 2=down, 3=left
DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]


def part1(infected_initial, bursts=10000):
    """Count infections after given bursts (simple rules)."""
    infected = set(infected_initial)
    x, y = 0, 0
    direction = 0  # Facing up
    infection_count = 0
    
    for _ in range(bursts):
        if (x, y) in infected:
            # Turn right
            direction = (direction + 1) % 4
            infected.remove((x, y))
        else:
            # Turn left
            direction = (direction - 1) % 4
            infected.add((x, y))
            infection_count += 1
        
        # Move forward
        x += DX[direction]
        y += DY[direction]
    
    return infection_count


# States for part 2
CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3


def part2(infected_initial, bursts=10000000):
    """Count infections after given bursts (evolved rules)."""
    # State: 0=clean, 1=weakened, 2=infected, 3=flagged
    state = {}
    for pos in infected_initial:
        state[pos] = INFECTED
    
    x, y = 0, 0
    direction = 0  # Facing up
    infection_count = 0
    
    for _ in range(bursts):
        current_state = state.get((x, y), CLEAN)
        
        if current_state == CLEAN:
            direction = (direction - 1) % 4  # Turn left
            state[(x, y)] = WEAKENED
        elif current_state == WEAKENED:
            # No turn
            state[(x, y)] = INFECTED
            infection_count += 1
        elif current_state == INFECTED:
            direction = (direction + 1) % 4  # Turn right
            state[(x, y)] = FLAGGED
        else:  # FLAGGED
            direction = (direction + 2) % 4  # Reverse
            del state[(x, y)]  # Clean
        
        # Move forward
        x += DX[direction]
        y += DY[direction]
    
    return infection_count


def run_example():
    example = """..#
#..
..."""
    infected = parse_input(example)
    assert part1(infected, 70) == 41
    assert part1(infected, 10000) == 5587
    print("Part 1 examples passed!")
    
    assert part2(infected, 100) == 26
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        infected = parse_input(f.read())
    
    print(f"Part 1: {part1(infected)}")
    print(f"Part 2: {part2(infected)}")

import os
import sys


def get_position(n):
    """Get (x, y) position of number n in the spiral. Position 1 is at (0,0)."""
    if n == 1:
        return (0, 0)
    
    # Find which ring the number is in
    # Ring k has side length 2k+1 and contains numbers up to (2k+1)^2
    k = 0
    while (2*k + 1) ** 2 < n:
        k += 1
    
    # Ring k starts at (2(k-1)+1)^2 + 1 = (2k-1)^2 + 1
    ring_start = (2*k - 1) ** 2 + 1
    ring_end = (2*k + 1) ** 2
    side_length = 2 * k
    
    # Position in ring (0-indexed from ring_start)
    pos = n - ring_start
    
    # Four sides: right, top, left, bottom
    # Right side: starts at (k, -(k-1)), goes up to (k, k)
    # Top side: starts at (k-1, k), goes left to (-k, k)
    # Left side: starts at (-k, k-1), goes down to (-k, -k)
    # Bottom side: starts at (-k+1, -k), goes right to (k, -k)
    
    if pos < side_length:  # Right side going up
        return (k, pos - k + 1)
    elif pos < 2 * side_length:  # Top side going left
        return (k - 1 - (pos - side_length), k)
    elif pos < 3 * side_length:  # Left side going down
        return (-k, k - 1 - (pos - 2 * side_length))
    else:  # Bottom side going right
        return (-k + 1 + (pos - 3 * side_length), -k)


def part1(n):
    """Manhattan distance from position n to center."""
    x, y = get_position(n)
    return abs(x) + abs(y)


def part2(target):
    """First value larger than target in the stress test spiral."""
    grid = {(0, 0): 1}
    x, y = 0, 0
    
    # Directions: right, up, left, down
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    
    direction = 0
    steps_in_direction = 1
    steps_taken = 0
    turns = 0
    
    while True:
        # Move
        x += dx[direction]
        y += dy[direction]
        steps_taken += 1
        
        # Calculate value as sum of all adjacent squares
        value = 0
        for ddx in [-1, 0, 1]:
            for ddy in [-1, 0, 1]:
                if (ddx, ddy) != (0, 0):
                    value += grid.get((x + ddx, y + ddy), 0)
        
        if value > target:
            return value
        
        grid[(x, y)] = value
        
        # Check if we need to turn
        if steps_taken == steps_in_direction:
            steps_taken = 0
            direction = (direction + 1) % 4
            turns += 1
            if turns % 2 == 0:
                steps_in_direction += 1


def run_example():
    # Part 1 examples
    assert part1(1) == 0
    assert part1(12) == 3
    assert part1(23) == 2
    assert part1(1024) == 31
    print("Part 1 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        n = int(f.read().strip())
    
    print(f"Part 1: {part1(n)}")
    print(f"Part 2: {part2(n)}")

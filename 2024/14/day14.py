import os
import sys
import re

def parse_input(text):
    """Parse the input to extract robot positions and velocities."""
    robots = []
    for line in text.strip().split('\n'):
        # Parse format: p=x,y v=vx,vy
        match = re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
        if match:
            x, y, vx, vy = map(int, match.groups())
            robots.append(((x, y), (vx, vy)))
    return robots

def simulate(robots, width, height, seconds):
    """Simulate robot movement for given seconds with wrapping."""
    final_positions = []
    for (x, y), (vx, vy) in robots:
        # Calculate final position with wrapping
        final_x = (x + vx * seconds) % width
        final_y = (y + vy * seconds) % height
        final_positions.append((final_x, final_y))
    return final_positions

def count_quadrants(positions, width, height):
    """Count robots in each quadrant, excluding middle lines."""
    mid_x = width // 2
    mid_y = height // 2

    quadrants = [0, 0, 0, 0]  # top-left, top-right, bottom-left, bottom-right

    for x, y in positions:
        # Skip robots exactly in the middle
        if x == mid_x or y == mid_y:
            continue

        # Determine quadrant
        if x < mid_x and y < mid_y:
            quadrants[0] += 1  # top-left
        elif x > mid_x and y < mid_y:
            quadrants[1] += 1  # top-right
        elif x < mid_x and y > mid_y:
            quadrants[2] += 1  # bottom-left
        else:  # x > mid_x and y > mid_y
            quadrants[3] += 1  # bottom-right

    return quadrants

def run_example():
    """Test with the example from the puzzle."""
    example = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

    robots = parse_input(example)
    print(f"Parsed {len(robots)} robots")
    print(f"First robot: {robots[0]}")

    # Example uses 11 wide, 7 tall
    width, height = 11, 7
    positions = simulate(robots, width, height, 100)

    quadrants = count_quadrants(positions, width, height)
    print(f"Quadrants: {quadrants}")

    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    print(f"Safety factor: {safety_factor}")
    print(f"Expected: 12")
    return safety_factor == 12

def part1():
    """Solve part 1."""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        text = f.read()

    robots = parse_input(text)

    # Real input uses 101 wide, 103 tall
    width, height = 101, 103
    positions = simulate(robots, width, height, 100)

    quadrants = count_quadrants(positions, width, height)

    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    return safety_factor

def visualize(positions, width, height):
    """Create a visual representation of robot positions."""
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        if grid[y][x] == '.':
            grid[y][x] = '1'
        else:
            grid[y][x] = str(min(9, int(grid[y][x]) + 1))
    return '\n'.join(''.join(row) for row in grid)

def has_large_cluster(positions, min_cluster_size=30):
    """Check if there's a large cluster of robots (potential tree pattern)."""
    position_set = set(positions)
    visited = set()

    def bfs(start):
        """Count connected robots using BFS."""
        queue = [start]
        visited.add(start)
        count = 1

        while queue:
            x, y = queue.pop(0)
            # Check 8-connected neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in position_set and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        count += 1
        return count

    for pos in positions:
        if pos not in visited:
            cluster_size = bfs(pos)
            if cluster_size >= min_cluster_size:
                return True
    return False

def has_symmetric_pattern(positions, width, height):
    """Check if positions form a somewhat symmetric pattern (like a tree)."""
    # Count robots in each row
    row_counts = {}
    for x, y in positions:
        row_counts[y] = row_counts.get(y, 0) + 1

    # Check if there's a concentration of robots in consecutive rows
    if len(row_counts) < 10:
        return False

    max_consecutive = 0
    current_consecutive = 0
    sorted_rows = sorted(row_counts.keys())

    for i in range(len(sorted_rows)):
        if row_counts[sorted_rows[i]] >= 3:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 0

    return max_consecutive >= 10

def part2():
    """Solve part 2 - find when robots form a Christmas tree."""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        text = f.read()

    robots = parse_input(text)
    width, height = 101, 103

    # Search for the Christmas tree pattern
    # Try up to 10000 seconds
    for seconds in range(1, 10000):
        positions = simulate(robots, width, height, seconds)

        # Check if robots form a large cluster (potential tree)
        if has_large_cluster(positions, min_cluster_size=100):
            # Print the visualization to verify
            print(f"\nPotential pattern at {seconds} seconds:")
            print(visualize(positions, width, height))
            return seconds

    return 0

if __name__ == "__main__":
    print("Testing example...")
    if run_example():
        print("✓ Example passed!\n")
    else:
        print("✗ Example failed!\n")

    print("Part 1:", part1())
    print("Part 2:", part2())

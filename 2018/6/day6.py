import sys
import os

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    coords = []
    for line in lines:
        x, y = map(int, line.strip().split(', '))
        coords.append((x, y))
    return coords

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve_part1(coords):
    if not coords:
        return 0

    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)

    # We only need to check the bounding box.
    # Closest points can be found by iterating over the grid.
    
    counts = {i: 0 for i in range(len(coords))}
    infinite_ids = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = []
            for i, (cx, cy) in enumerate(coords):
                dist = manhattan((x, y), (cx, cy))
                distances.append((dist, i))
            
            distances.sort()
            
            # Check for tie
            if len(distances) > 1 and distances[0][0] == distances[1][0]:
                continue
            
            closest_id = distances[0][1]
            counts[closest_id] += 1
            
            # Check if on boundary
            if x == min_x or x == max_x or y == min_y or y == max_y:
                infinite_ids.add(closest_id)

    # Filter out infinite areas
    max_area = 0
    for i in counts:
        if i not in infinite_ids:
            max_area = max(max_area, counts[i])
            
    return max_area

def solve_part2(coords, threshold):
    if not coords:
        return 0

    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)
    
    # Expand search area slightly to be safe, though strict bounding box is usually enough
    # The max possible reach is threshold / len(coords) from the bounding box
    margin = int(threshold / len(coords)) + 1
    
    region_size = 0
    for x in range(min_x - margin, max_x + margin + 1):
        for y in range(min_y - margin, max_y + margin + 1):
            total_dist = sum(manhattan((x, y), c) for c in coords)
            if total_dist < threshold:
                region_size += 1
                
    return region_size

def part1():
    coords = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part1(coords)
    print(f'Part 1: {result}')
    return result

def part2():
    coords = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part2(coords, 10000)
    print(f'Part 2: {result}')
    return result

def run_example():
    print("Running Example...")
    example_coords = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9)
    ]
    # Example logic verification
    p1_result = solve_part1(example_coords)
    print(f"Example Part 1 Result: {p1_result}")
    assert p1_result == 17
    
    p2_result = solve_part2(example_coords, 32)
    print(f"Example Part 2 Result: {p2_result}")
    assert p2_result == 16

if __name__ == '__main__':
    run_example()
    part1()
    part2()

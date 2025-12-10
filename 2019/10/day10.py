
import sys
import os
import math
from collections import defaultdict

def parse_map(data):
    asteroids = []
    lines = data.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.append((x, y))
    return asteroids

def get_angle(origin, target):
    # Returns angle in radians, but we can use (dx, dy) simplified GCD
    # Actually, iterate all other asteroids, calculate angle
    # A set of unique angles = number of visible asteroids
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    return math.atan2(dy, dx)

def count_visible(origin, asteroids):
    angles = set()
    for target in asteroids:
        if origin == target:
            continue
        angle = get_angle(origin, target)
        angles.add(angle)
    return len(angles)

def solve_part1(data):
    asteroids = parse_map(data)
    max_visible = 0
    best_station = None
    
    for station in asteroids:
        count = count_visible(station, asteroids)
        if count > max_visible:
            max_visible = count
            best_station = station
            
    return max_visible, best_station

def solve_part2(data, station):
    asteroids = parse_map(data)
    # Group asteroids by angle
    targets_by_angle = defaultdict(list)
    
    for target in asteroids:
        if station == target:
            continue
        
        dx = target[0] - station[0]
        dy = target[1] - station[1]
        
        # Calculate angle. 
        # ATAN2 returns angle from -pi to pi.
        # 0 is right (positive x), pi/2 is down (positive y in our grid?), -pi/2 is up.
        # We need to start from UP (0 degrees or -pi/2 in atan2) and rotate clockwise.
        
        # Standard atan2(y, x):
        # 0 -> Right
        # pi/2 -> Down
        # pi -> Left
        # -pi/2 -> Up
        
        angle = math.atan2(dy, dx)
        
        # Convert to 0-2pi range starting from UP (-pi/2) going clockwise
        # Up (-pi/2) should be 0
        # Right (0) should be pi/2
        # Down (pi/2) should be pi
        # Left (pi or -pi) should be 3pi/2
        
        # Current atan2:
        # Up: -pi/2 -> wanted 0.  Add pi/2 => 0
        # Right: 0 -> wanted pi/2. Add pi/2 => pi/2
        # Down: pi/2 -> wanted pi. Add pi/2 => pi
        # Left: pi -> wanted 3pi/2. Add pi/2 => 3pi/2
        # Left: -pi -> wanted 3pi/2. Add pi/2 => -pi/2 (add 2pi => 3pi/2)
        
        adjusted_angle = angle + math.pi/2
        if adjusted_angle < 0:
            adjusted_angle += 2 * math.pi
            
        dist = math.sqrt(dx*dx + dy*dy)
        targets_by_angle[adjusted_angle].append((dist, target))
        
    # Sort targets at each angle by distance (closest first)
    sorted_angles = sorted(targets_by_angle.keys())
    for angle in sorted_angles:
        targets_by_angle[angle].sort(key=lambda x: x[0])
        
    vaporized_count = 0
    last_vaporized = None
    
    # Sweep around
    while vaporized_count < 200 and targets_by_angle:
        # It's possible we run out of asteroids before 200 if input is small (not for real input)
        empty_angles = []
        for angle in sorted_angles:
            if targets_by_angle[angle]:
                # Vaporize closest
                _, target = targets_by_angle[angle].pop(0)
                vaporized_count += 1
                last_vaporized = target
                
                if vaporized_count == 200:
                    return last_vaporized[0] * 100 + last_vaporized[1]
            else:
                empty_angles.append(angle) # Should not happen if we check emptiness, but just in case
                
    return 0 # Should check if we found it

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    max_visible, best_station = solve_part1(data)
    print("Part 1:", max_visible)
    # We need to uncomment part 2 logic once we know the prompt, but usually it involves the 200th asteroid
    # Prompt not fully read for Part 2 yet, but usually standard. I'll read puzzle.md Part 2 first.
    # Actually I can't read Part 2 yet. But I can prepare the function.
    # Let's print Part 1 only first.
    print("Part 2:", solve_part2(data, best_station))

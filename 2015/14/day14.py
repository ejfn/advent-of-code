import os
import sys
import re

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_reindeer(lines):
    reindeer = []
    for line in lines:
        m = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.', line)
        name = m.group(1)
        speed = int(m.group(2))
        fly_time = int(m.group(3))
        rest_time = int(m.group(4))
        reindeer.append((name, speed, fly_time, rest_time))
    return reindeer

def distance_at_time(speed, fly_time, rest_time, total_time):
    cycle = fly_time + rest_time
    full_cycles = total_time // cycle
    remaining = total_time % cycle
    fly_remaining = min(remaining, fly_time)
    return speed * (full_cycles * fly_time + fly_remaining)

def part1(lines):
    reindeer = parse_reindeer(lines)
    return max(distance_at_time(speed, fly_time, rest_time, 2503) 
               for name, speed, fly_time, rest_time in reindeer)

def part2(lines):
    reindeer = parse_reindeer(lines)
    points = {name: 0 for name, _, _, _ in reindeer}
    
    for t in range(1, 2504):
        distances = {name: distance_at_time(speed, fly_time, rest_time, t) 
                     for name, speed, fly_time, rest_time in reindeer}
        max_dist = max(distances.values())
        for name, dist in distances.items():
            if dist == max_dist:
                points[name] += 1
    
    return max(points.values())

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

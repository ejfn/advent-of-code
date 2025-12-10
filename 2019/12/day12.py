
import sys
import os
import re
import math
from itertools import count

# Helper for LCM
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def parse_input(data):
    moons = []
    # Format: <x=-1, y=0, z=2>
    pattern = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
    for line in data.strip().split('\n'):
        match = pattern.match(line)
        if match:
            pos = list(map(int, match.groups()))
            vel = [0, 0, 0]
            moons.append({'pos': pos, 'vel': vel})
    return moons

def step_simulation(moons):
    # Apply gravity
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            m1 = moons[i]
            m2 = moons[j]
            for axis in range(3):
                if m1['pos'][axis] < m2['pos'][axis]:
                    m1['vel'][axis] += 1
                    m2['vel'][axis] -= 1
                elif m1['pos'][axis] > m2['pos'][axis]:
                    m1['vel'][axis] -= 1
                    m2['vel'][axis] += 1
    
    # Apply velocity
    for m in moons:
        for axis in range(3):
            m['pos'][axis] += m['vel'][axis]

def solve_part1(data):
    moons = parse_input(data)
    for _ in range(1000):
        step_simulation(moons)
        
    total_energy = 0
    for m in moons:
        pot = sum(abs(x) for x in m['pos'])
        kin = sum(abs(x) for x in m['vel'])
        total_energy += pot * kin
        
    return total_energy

def solve_part2(data):
    # The axes are independent!
    # We can find the cycle length for X, Y, and Z independently, then LCM them.
    
    initial_moons = parse_input(data)
    # Extract just the 1D state for each axis
    # State = (pos1, pos2, pos3, pos4, vel1, vel2, vel3, vel4)
    
    cycle_lengths = []
    
    for axis in range(3):
        # Initial state for this axis
        positions = [m['pos'][axis] for m in initial_moons]
        velocities = [0] * len(initial_moons)
        
        initial_state = tuple(positions + velocities)
        
        steps = 0
        while True:
            # Gravity
            for i in range(len(positions)):
                for j in range(i+1, len(positions)):
                    if positions[i] < positions[j]:
                        velocities[i] += 1
                        velocities[j] -= 1
                    elif positions[i] > positions[j]:
                        velocities[i] -= 1
                        velocities[j] += 1
            
            # Velocity
            for i in range(len(positions)):
                positions[i] += velocities[i]
            
            steps += 1
            
            curr_state = tuple(positions + velocities)
            if curr_state == initial_state:
                cycle_lengths.append(steps)
                break
                
    # LCM of the 3 cycle lengths
    result = cycle_lengths[0]
    for c in cycle_lengths[1:]:
        result = lcm(result, c)
        
    return result

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

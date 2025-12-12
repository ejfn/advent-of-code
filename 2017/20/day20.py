import os
import sys
import re
from collections import defaultdict


def parse_input(text):
    """Parse particles into list of (pos, vel, acc) tuples."""
    particles = []
    for line in text.strip().split('\n'):
        if not line.strip():
            continue
        # Extract numbers
        nums = list(map(int, re.findall(r'-?\d+', line)))
        pos = tuple(nums[0:3])
        vel = tuple(nums[3:6])
        acc = tuple(nums[6:9])
        particles.append([list(pos), list(vel), list(acc)])
    return particles


def manhattan(v):
    return sum(abs(x) for x in v)


def part1(particles):
    """Find particle that stays closest to origin long-term.
    
    In the long term, acceleration dominates. The particle with
    smallest total acceleration (sum of absolute values) stays closest.
    If tied, compare velocity, then position.
    """
    def key(idx):
        p, v, a = particles[idx]
        return (manhattan(a), manhattan(v), manhattan(p))
    
    return min(range(len(particles)), key=key)


def step(particles):
    """Simulate one tick."""
    for p in particles:
        pos, vel, acc = p
        for i in range(3):
            vel[i] += acc[i]
            pos[i] += vel[i]


def remove_collisions(particles):
    """Remove all particles that collide."""
    # Count positions
    positions = defaultdict(list)
    for i, p in enumerate(particles):
        positions[tuple(p[0])].append(i)
    
    # Find colliding indices
    to_remove = set()
    for pos, indices in positions.items():
        if len(indices) > 1:
            to_remove.update(indices)
    
    # Remove in reverse order
    for i in sorted(to_remove, reverse=True):
        del particles[i]


def part2(particles):
    """Count particles after all collisions.
    
    Simulate until no more collisions happen for a while.
    """
    # Make a copy so we don't modify original
    particles = [[list(p), list(v), list(a)] for p, v, a in particles]
    
    no_collision_rounds = 0
    prev_count = len(particles)
    
    while no_collision_rounds < 100:  # If no collisions for 100 rounds, assume done
        step(particles)
        remove_collisions(particles)
        
        if len(particles) == prev_count:
            no_collision_rounds += 1
        else:
            no_collision_rounds = 0
            prev_count = len(particles)
    
    return len(particles)


def run_example():
    example1 = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""
    particles = parse_input(example1)
    assert part1(particles) == 0
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        particles = parse_input(f.read())
    
    print(f"Part 1: {part1(particles)}")
    print(f"Part 2: {part2(particles)}")

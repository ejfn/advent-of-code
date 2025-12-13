import os
import sys
import re
from itertools import permutations

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_happiness(lines):
    happiness = {}
    people = set()
    for line in lines:
        m = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.', line)
        person = m.group(1)
        gain_lose = m.group(2)
        amount = int(m.group(3))
        neighbor = m.group(4)
        if gain_lose == 'lose':
            amount = -amount
        happiness[(person, neighbor)] = amount
        people.add(person)
    return happiness, list(people)

def calculate_happiness(arrangement, happiness):
    total = 0
    n = len(arrangement)
    for i in range(n):
        left = arrangement[(i - 1) % n]
        right = arrangement[(i + 1) % n]
        person = arrangement[i]
        total += happiness.get((person, left), 0)
        total += happiness.get((person, right), 0)
    return total

def part1(lines):
    happiness, people = parse_happiness(lines)
    # Fix one person to avoid circular duplicates
    first = people[0]
    others = people[1:]
    max_happiness = max(calculate_happiness([first] + list(perm), happiness) for perm in permutations(others))
    return max_happiness

def part2(lines):
    happiness, people = parse_happiness(lines)
    # Add yourself with 0 happiness change to everyone
    for person in people:
        happiness[('You', person)] = 0
        happiness[(person, 'You')] = 0
    people.append('You')
    
    first = 'You'  # Use myself as the fixed person
    others = [p for p in people if p != 'You']
    max_happiness = max(calculate_happiness([first] + list(perm), happiness) for perm in permutations(others))
    return max_happiness

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

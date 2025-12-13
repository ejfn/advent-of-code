import os
import sys
from itertools import permutations

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_distances(lines):
    distances = {}
    cities = set()
    for line in lines:
        parts = line.split(' = ')
        dist = int(parts[1])
        route = parts[0].split(' to ')
        a, b = route[0], route[1]
        cities.add(a)
        cities.add(b)
        distances[(a, b)] = dist
        distances[(b, a)] = dist
    return distances, list(cities)

def route_distance(route, distances):
    total = 0
    for i in range(len(route) - 1):
        total += distances[(route[i], route[i+1])]
    return total

def part1(lines):
    distances, cities = parse_distances(lines)
    return min(route_distance(perm, distances) for perm in permutations(cities))

def part2(lines):
    distances, cities = parse_distances(lines)
    return max(route_distance(perm, distances) for perm in permutations(cities))

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

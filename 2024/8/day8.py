import os
import sys
from collections import defaultdict

def parse_input(filename):
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f]

def part1():
    grid = parse_input(os.path.join(sys.path[0], 'input.txt'))
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Group antennas by frequency
    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '.':
                antennas[grid[r][c]].append((r, c))

    # Find all antinodes
    antinodes = set()

    for freq, positions in antennas.items():
        # For each pair of antennas with same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # Calculate the difference vector
                dr = r2 - r1
                dc = c2 - c1

                # Antinode 1: beyond antenna 2 (antenna 1 is closer)
                # This is where antenna 2 is twice as close as antenna 1
                antinode1 = (r2 + dr, c2 + dc)

                # Antinode 2: beyond antenna 1 (antenna 2 is closer)
                # This is where antenna 1 is twice as close as antenna 2
                antinode2 = (r1 - dr, c1 - dc)

                # Check if antinodes are within bounds
                if 0 <= antinode1[0] < rows and 0 <= antinode1[1] < cols:
                    antinodes.add(antinode1)

                if 0 <= antinode2[0] < rows and 0 <= antinode2[1] < cols:
                    antinodes.add(antinode2)

    return len(antinodes)

def part2():
    grid = parse_input(os.path.join(sys.path[0], 'input.txt'))
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Group antennas by frequency
    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '.':
                antennas[grid[r][c]].append((r, c))

    # Find all antinodes
    antinodes = set()

    for freq, positions in antennas.items():
        # For each pair of antennas with same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # Calculate the difference vector
                dr = r2 - r1
                dc = c2 - c1

                # Add all points in line with these two antennas
                # Start from antenna 1 and go backwards
                r, c = r1, c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r -= dr
                    c -= dc

                # Start from antenna 1 and go forwards
                r, c = r1, c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r += dr
                    c += dc

    return len(antinodes)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

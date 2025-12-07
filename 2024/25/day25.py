import os
import sys

def parse_input(filename):
    """Parse the input file and separate locks and keys."""
    with open(filename) as f:
        content = f.read().strip()

    schematics = content.split('\n\n')
    locks = []
    keys = []

    for schematic in schematics:
        lines = schematic.split('\n')

        # Check if it's a lock (top row all #) or key (top row all .)
        if lines[0] == '#####':
            # It's a lock - count heights from top
            heights = []
            for col in range(5):
                height = 0
                for row in range(1, 7):  # Skip the top row
                    if lines[row][col] == '#':
                        height += 1
                    else:
                        break
                heights.append(height)
            locks.append(tuple(heights))
        else:
            # It's a key - count heights from bottom
            heights = []
            for col in range(5):
                height = 0
                for row in range(5, 0, -1):  # Skip the bottom row, go upward
                    if lines[row][col] == '#':
                        height += 1
                    else:
                        break
                heights.append(height)
            keys.append(tuple(heights))

    return locks, keys

def fits(lock, key):
    """Check if a key fits a lock (no overlap)."""
    # Available space is 5 (6 rows minus top and bottom)
    for i in range(5):
        if lock[i] + key[i] > 5:
            return False
    return True

def part1():
    """Count unique lock/key pairs that fit together."""
    locks, keys = parse_input(os.path.join(sys.path[0], 'input.txt'))

    count = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                count += 1

    return count

def part2():
    """Part 2 - Day 25 has no Part 2 puzzle, automatically completed!"""
    return "⭐ All 50 stars collected! Merry Christmas!"

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

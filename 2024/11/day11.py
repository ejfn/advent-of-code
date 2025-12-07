import os
import sys
from collections import Counter

def load_input():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        return list(map(int, f.read().strip().split()))

def blink_stone(stone):
    """Apply transformation rules to a single stone, return list of resulting stones."""
    if stone == 0:
        return [1]

    # Check if even number of digits
    stone_str = str(stone)
    num_digits = len(stone_str)

    if num_digits % 2 == 0:
        # Split in half
        mid = num_digits // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])
        return [left, right]

    # Multiply by 2024
    return [stone * 2024]

def simulate_blinks_naive(stones, num_blinks):
    """Simulate blinks by tracking the list of stones."""
    current = stones[:]
    for _ in range(num_blinks):
        next_stones = []
        for stone in current:
            next_stones.extend(blink_stone(stone))
        current = next_stones
    return len(current)

def simulate_blinks_optimized(stones, num_blinks):
    """Simulate blinks by counting occurrences of each stone value."""
    # Use a counter to track how many of each stone value we have
    stone_counts = Counter(stones)

    for _ in range(num_blinks):
        next_counts = Counter()
        for stone, count in stone_counts.items():
            # Apply transformation to this stone value
            new_stones = blink_stone(stone)
            for new_stone in new_stones:
                next_counts[new_stone] += count
        stone_counts = next_counts

    return sum(stone_counts.values())

def part1():
    stones = load_input()
    return simulate_blinks_optimized(stones, 25)

def part2():
    stones = load_input()
    return simulate_blinks_optimized(stones, 75)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

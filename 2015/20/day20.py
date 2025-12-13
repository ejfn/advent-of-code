import os
import sys

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return int(f.read().strip())

def part1(target):
    # Find lowest house number with at least target presents
    # Each house h gets 10 * sum of divisors of h
    limit = target // 10
    presents = [0] * (limit + 1)
    
    for elf in range(1, limit + 1):
        for house in range(elf, limit + 1, elf):
            presents[house] += elf * 10
    
    for house, p in enumerate(presents):
        if p >= target:
            return house
    return None

def part2(target):
    # Each elf visits at most 50 houses, delivers 11 presents
    limit = target // 10
    presents = [0] * (limit + 1)
    
    for elf in range(1, limit + 1):
        for i, house in enumerate(range(elf, limit + 1, elf)):
            if i >= 50:
                break
            presents[house] += elf * 11
    
    for house, p in enumerate(presents):
        if p >= target:
            return house
    return None

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

import os
import sys


def redistribute(banks):
    """Redistribute blocks from the largest bank."""
    n = len(banks)
    # Find bank with most blocks (lowest index wins ties)
    max_val = max(banks)
    idx = banks.index(max_val)
    
    blocks = banks[idx]
    banks[idx] = 0
    
    # Distribute blocks one at a time starting from next bank
    while blocks > 0:
        idx = (idx + 1) % n
        banks[idx] += 1
        blocks -= 1
    
    return banks


def solve(banks_orig):
    """Returns (cycles to first repeat, cycle length)."""
    banks = list(banks_orig)
    seen = {tuple(banks): 0}
    cycles = 0
    
    while True:
        banks = redistribute(banks)
        cycles += 1
        
        state = tuple(banks)
        if state in seen:
            return cycles, cycles - seen[state]
        
        seen[state] = cycles


def part1(banks):
    return solve(banks)[0]


def part2(banks):
    return solve(banks)[1]


def run_example():
    example = [0, 2, 7, 0]
    assert part1(example) == 5
    print("Part 1 example passed!")
    assert part2(example) == 4
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        banks = [int(x) for x in f.read().split()]
    
    print(f"Part 1: {part1(banks)}")
    print(f"Part 2: {part2(banks)}")

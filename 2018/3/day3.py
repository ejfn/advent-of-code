import os
import sys
import re
from collections import defaultdict

def load_input(filename):
    """Load claims from input file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def parse_claim(claim_str):
    """Parse claim string like '#1 @ 3,2: 5x4' into (id, x, y, w, h)."""
    match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim_str)
    if not match:
        raise ValueError(f"Invalid claim format: {claim_str}")
    return tuple(map(int, match.groups()))

def part1(claims):
    """Count square inches with 2+ overlapping claims."""
    fabric = defaultdict(int)
    
    for claim_str in claims:
        claim_id, x, y, w, h = parse_claim(claim_str)
        for i in range(x, x + w):
            for j in range(y, y + h):
                fabric[(i, j)] += 1
    
    # Count squares with 2+ claims
    return sum(1 for count in fabric.values() if count >= 2)

def part2(claims):
    """Find the ID of the only claim that doesn't overlap."""
    fabric = defaultdict(int)
    parsed_claims = []
    
    # Mark all squares
    for claim_str in claims:
        claim_id, x, y, w, h = parse_claim(claim_str)
        parsed_claims.append((claim_id, x, y, w, h))
        for i in range(x, x + w):
            for j in range(y, y + h):
                fabric[(i, j)] += 1
    
    # Find claim with no overlaps
    for claim_id, x, y, w, h in parsed_claims:
        has_overlap = False
        for i in range(x, x + w):
            for j in range(y, y + h):
                if fabric[(i, j)] > 1:
                    has_overlap = True
                    break
            if has_overlap:
                break
        if not has_overlap:
            return claim_id
    
    raise ValueError("No non-overlapping claim found")

def run_example():
    """Run example from puzzle."""
    example = [
        "#1 @ 1,3: 4x4",
        "#2 @ 3,1: 4x4",
        "#3 @ 5,5: 2x2"
    ]
    print("Part 1 example:", part1(example))
    print("(Expected: 4 square inches)")
    print("Part 2 example:", part2(example))
    print("(Expected: 3)")

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    try:
        claims = load_input(input_path)
        print("Part 1:", part1(claims))
        print("Part 2:", part2(claims))
    except FileNotFoundError:
        print("input.txt not found. Running examples:")
        run_example()

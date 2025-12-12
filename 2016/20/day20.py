import sys
import os

def parse_ranges(lines):
    ranges = []
    for line in lines:
        if not line.strip():
            continue
        start, end = map(int, line.strip().split('-'))
        ranges.append((start, end))
    return ranges

def solve(ranges, max_ip):
    # Sort by start time
    ranges.sort(key=lambda x: x[0])
    
    candidate = 0
    valid_count = 0
    lowest_valid = None
    
    for start, end in ranges:
        if start > candidate:
            # Found a gap
            if lowest_valid is None:
                lowest_valid = candidate
            
            valid_count += (start - candidate)
            candidate = end + 1
        else:
            # Overlap or contiguous
            candidate = max(candidate, end + 1)
            
    # Check tail
    if candidate <= max_ip:
        if lowest_valid is None:
            lowest_valid = candidate
        valid_count += (max_ip - candidate + 1)
        
    return lowest_valid, valid_count

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    ranges = parse_ranges(lines)
    lowest, _ = solve(ranges, 4294967295)
    return lowest

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    ranges = parse_ranges(lines)
    _, count = solve(ranges, 4294967295)
    return count

def run_example():
    # Example ranges: 5-8, 0-2, 4-7
    # Allowed: 3, 9. (Max 9)
    raw = ["5-8", "0-2", "4-7"]
    ranges = parse_ranges(raw)
    lowest, count = solve(ranges, 9)
    print(f"Example (Max 9): Lowest={lowest} (Expected 3), Count={count} (Expected 2)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

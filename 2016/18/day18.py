import sys
import os

def solve(initial_row, total_rows):
    current_row = initial_row
    width = len(initial_row)
    safe_count = current_row.count('.')
    
    # Pre-compute next row generation
    # Actually, iterating 400,000 times for width 100 is fast.
    # 4e5 * 100 = 4e7 ops.
    # In Python, string construction might be slow.
    # Let's use list of booleans? True for Trap (^), False for Safe (.).
    # Or just keep it as string if efficient.
    # String manipulation is optimized in C.
    
    # 0 = '.', 1 = '^'
    # row = [1 if c == '^' else 0 for c in initial_row]
    # safe_count = row.count(0)
    
    # Let's try string approach first, it's easier to read/debug.
    # If slow, we optimize.
    
    for _ in range(total_rows - 1):
        # Calculate next row
        # Left neighbor: [safe] + row[:-1]
        # Right neighbor: row[1:] + [safe]
        # Trap if L != R (XOR)
        
        # Using string slicing and zip
        lefts = '.' + current_row[:-1]
        rights = current_row[1:] + '.'
        
        new_row = []
        for l, r in zip(lefts, rights):
            if l != r: # One is trap, one is safe -> New is trap
                new_row.append('^')
            else:
                new_row.append('.')
        
        current_row = "".join(new_row)
        safe_count += current_row.count('.')
        
    return safe_count

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        initial_row = f.read().strip()
    return solve(initial_row, 40)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        initial_row = f.read().strip()
    return solve(initial_row, 400000)

def run_example():
    # Example 1: ..^^. (5 cols) -> 3 rows -> 6 safe tiles.
    # But wait, example says:
    # ..^^.
    # .^^^^
    # ^^..^
    # Safe counts: 3 + 1 + 2 = 6.
    
    row = "..^^."
    print(f"Small Example (3 rows): {solve(row, 3)} (Expected 6)")
    
    # Larger example: .^^.^.^^^^ (10 cols) -> 10 rows -> 38 safe.
    row2 = ".^^.^.^^^^"
    print(f"Large Example (10 rows): {solve(row2, 10)} (Expected 38)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        # Part 2 is not unlocked yet officially but is predictable from typical AoC patterns.
        # I'll include it.
        print("Part 2:", part2())

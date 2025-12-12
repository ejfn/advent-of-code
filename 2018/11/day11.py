
import sys
import os

def get_power_level(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    digit = (power // 100) % 10
    return digit - 5

def build_sat(grid):
    height = len(grid)
    width = len(grid[0])
    sat = [[0 for _ in range(width + 1)] for _ in range(height + 1)]
    
    for y in range(height):
        for x in range(width):
            sat[y+1][x+1] = grid[y][x] + sat[y][x+1] + sat[y+1][x] - sat[y][x]
            
    return sat

def get_sum(sat, x, y, size):
    # x, y are 1-based top-left coordinates in the original grid
    # sat uses 1-based indexing for the grid
    # sum(x, y, size) means sum from (x, y) to (x+size-1, y+size-1)
    
    # x1, y1 correspond to sat indices x, y
    # x2, y2 correspond to sat indices x+size, y+size
    
    x0 = x - 1
    y0 = y - 1
    x1 = x + size - 1
    y1 = y + size - 1
    
    return sat[y1][x1] - sat[y0][x1] - sat[y1][x0] + sat[y0][x0]

def solve_for_serial(serial):
    grid_size = 300
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for y in range(grid_size):
        for x in range(grid_size):
            grid[y][x] = get_power_level(x + 1, y + 1, serial)
            
    sat = build_sat(grid)
    
    best_power = float('-inf')
    best_coord = None
    
    for y in range(1, grid_size - 3 + 2):
        for x in range(1, grid_size - 3 + 2):
            s = get_sum(sat, x, y, 3)
            if s > best_power:
                best_power = s
                best_coord = (x, y)
                
    return best_coord

def part1(serial):
    x, y = solve_for_serial(serial)
    return f"{x},{y}"

def solve_part2(serial):
    grid_size = 300
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for y in range(grid_size):
        for x in range(grid_size):
            grid[y][x] = get_power_level(x + 1, y + 1, serial)
            
    sat = build_sat(grid)
    
    best_power = float('-inf')
    best_combo = None
    
    # Check all sizes
    for size in range(1, grid_size + 1):
        # Optimization: Early exit if we have found a very good solution? 
        # No, because a larger square might include many positive numbers.
        # But we can perhaps skip sizes if power is decreasing? Not guaranteed.
        # Just brute force with SAT.
        
        for y in range(1, grid_size - size + 2):
            for x in range(1, grid_size - size + 2):
                s = get_sum(sat, x, y, size)
                if s > best_power:
                    best_power = s
                    best_combo = (x, y, size)

    return best_combo

def part1(serial):
    x, y = solve_for_serial(serial)
    return f"{x},{y}"

def part2(serial):
    x, y, size = solve_part2(serial)
    return f"{x},{y},{size}"

def run_example():
    print("Running examples...")
    p1 = get_power_level(3, 5, 8)
    print(f"Power(3, 5, 8) = {p1} (Expected 4)")
    assert p1 == 4
    
    assert get_power_level(122, 79, 57) == -5
    assert get_power_level(217, 196, 39) == 0
    assert get_power_level(101, 153, 71) == 4
    
    res18 = solve_for_serial(18)
    print(f"Serial 18 best 3x3: {res18} (Expected 33, 45)")
    assert res18 == (33, 45)

    res42 = solve_for_serial(42)
    print(f"Serial 42 best 3x3: {res42} (Expected 21, 61)")
    assert res42 == (21, 61)
    
    # Part 2 examples
    # Validating full Part 2 on examples might be slowish, but useful.
    # Expected: 90,269,16
    print("Running Part 2 example for serial 18 (might take a few seconds)...")
    res18_2 = solve_part2(18)
    print(f"Serial 18 best square: {res18_2} (Expected 90, 269, 16)")
    assert res18_2 == (90, 269, 16)
    
    print("Running Part 2 example for serial 42...")
    res42_2 = solve_part2(42)
    print(f"Serial 42 best square: {res42_2} (Expected 232, 251, 12)")
    assert res42_2 == (232, 251, 12)
    
    print("Examples passed!")

if __name__ == '__main__':
    run_example()
    
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        serial = int(f.read().strip())
    
    print(f"Part 1: {part1(serial)}")
    print(f"Part 2: {part2(serial)}")


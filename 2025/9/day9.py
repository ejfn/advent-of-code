import os
import sys

def parse_input(filename):
    """Parse the input file and return list of (x, y) coordinates"""
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    coords = []
    for line in lines:
        x, y = map(int, line.split(','))
        coords.append((x, y))

    return coords

def find_largest_rectangle(coords):
    """Find the largest rectangle area using two red tiles as opposite corners"""
    max_area = 0

    # Try all pairs of coordinates as opposite corners
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            # Calculate the area of the rectangle
            # The corners must be opposite, meaning different x AND different y
            if x1 != x2 and y1 != y2:
                # The rectangle includes all tiles from (min_x, min_y) to (max_x, max_y)
                # Since tiles are discrete units, we add 1 to each dimension
                width = abs(x2 - x1) + 1
                height = abs(y2 - y1) + 1
                area = width * height
                max_area = max(max_area, area)

    return max_area

def run_example():
    """Test with the example from the puzzle"""
    example_coords = [
        (7, 1),
        (11, 1),
        (11, 7),
        (9, 7),
        (9, 5),
        (2, 5),
        (2, 3),
        (7, 3)
    ]

    print("Example coordinates:")
    for coord in example_coords:
        print(f"  {coord}")
    print(f"Number of red tiles: {len(example_coords)}")

    result = find_largest_rectangle(example_coords)
    print(f"\nExample result: {result}")
    print(f"Expected: 50")

    # Let's verify some specific rectangles mentioned in the problem
    # Between 2,5 and 9,7: width=7, height=2, area=14... wait that doesn't match
    # Actually let me recalculate: (2,5) to (9,7)
    # width = |9-2| = 7, height = |7-5| = 2, area = 14... but problem says 24

    # Ah! The problem says area 24 which is 8*3... let me check coordinates
    # Looking at the grid, 2,5 to 9,7 spans from column 2 to 9 (8 columns) and row 5 to 7 (3 rows)
    # So area = 8 * 3 = 24. But abs(9-2) = 7, not 8!

    # I think the issue is that tiles span a unit area, so distance includes both endpoints
    # So width should be |x2-x1| and height should be |y2-y1| (already calculated correctly for continuous space)
    # Let me verify: 2,5 to 9,7 -> |9-2| * |7-5| = 7 * 2 = 14, not 24

    # Wait, looking more carefully at the grid display:
    # Row 5: ..OOOOOOOO.... (starts at col 2, 8 O's)
    # Row 6: ..OOOOOOOO....
    # Row 7: ..OOOOOOOO.#..
    # So it's 8 wide and 3 tall = 24

    # The rectangle from (2,5) to (9,7) includes columns 2,3,4,5,6,7,8,9 (8 columns)
    # and rows 5,6,7 (3 rows). So we need to ADD 1 to each dimension!

    return result == 50

def part1():
    """Solve part 1"""
    input_file = os.path.join(sys.path[0], 'input.txt')
    coords = parse_input(input_file)
    return find_largest_rectangle(coords)

def part2():
    """Solve part 2"""
    input_file = os.path.join(sys.path[0], 'input.txt')
    coords = parse_input(input_file)
    # Part 2 logic will be added after part 1 is solved
    return 0

if __name__ == "__main__":
    # Test with example first
    print("=" * 50)
    print("Testing with example:")
    print("=" * 50)
    run_example()

    print("\n" + "=" * 50)
    print("Part 1:")
    print("=" * 50)
    result1 = part1()
    print(result1)

    print("\n" + "=" * 50)
    print("Part 2:")
    print("=" * 50)
    result2 = part2()
    print(result2)

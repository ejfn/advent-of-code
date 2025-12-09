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

def is_inside_polygon(point, polygon):
    """Check if point is inside polygon using ray casting algorithm"""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def find_largest_rectangle_with_green(coords):
    """
    Find largest rectangle with red corners containing only red/green tiles.

    Uses scanline approach: for each y, compute valid x-range [left, right].
    A rectangle is valid if for all rows, x fits within valid range.
    Use sparse table for O(1) range-max/min queries.
    """
    import math

    n = len(coords)

    # Build boundary edges (horizontal and vertical segments)
    # Each edge is ((x1, y1), (x2, y2)) where x1<=x2 and y1<=y2
    h_edges = []  # horizontal edges (same y)
    v_edges = []  # vertical edges (same x)

    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]

        if y1 == y2:  # horizontal edge
            h_edges.append((min(x1, x2), max(x1, x2), y1))
        else:  # vertical edge
            v_edges.append((x1, min(y1, y2), max(y1, y2)))

    # Get all unique y-coordinates from red tiles
    y_coords = sorted(set(coord[1] for coord in coords))
    y_to_idx = {y: i for i, y in enumerate(y_coords)}

    # For each y-level, compute [left_bound, right_bound] of valid region
    # Using scanline: count crossings of vertical edges
    left_bounds = {}
    right_bounds = {}

    for y in y_coords:
        # Find all vertical edges that span this y
        crossings = []
        for vx, vy1, vy2 in v_edges:
            if vy1 <= y <= vy2:
                crossings.append(vx)
        crossings.sort()

        # Use even-odd rule: inside between pairs of crossings
        # For rectilinear polygon, first crossing is left bound, second is right
        if len(crossings) >= 2:
            left_bounds[y] = crossings[0]
            right_bounds[y] = crossings[-1]
        else:
            left_bounds[y] = float('inf')
            right_bounds[y] = float('-inf')

    # Build sparse table for range-max of left_bounds and range-min of right_bounds
    m = len(y_coords)
    if m == 0:
        return 0

    log_m = max(1, int(math.log2(m)) + 1)

    # Sparse table for range-max of left_bounds
    left_arr = [left_bounds.get(y, float('inf')) for y in y_coords]
    max_left = [[0] * m for _ in range(log_m)]
    max_left[0] = left_arr[:]

    for j in range(1, log_m):
        for i in range(m - (1 << j) + 1):
            max_left[j][i] = max(max_left[j-1][i], max_left[j-1][i + (1 << (j-1))])

    # Sparse table for range-min of right_bounds
    right_arr = [right_bounds.get(y, float('-inf')) for y in y_coords]
    min_right = [[0] * m for _ in range(log_m)]
    min_right[0] = right_arr[:]

    for j in range(1, log_m):
        for i in range(m - (1 << j) + 1):
            min_right[j][i] = min(min_right[j-1][i], min_right[j-1][i + (1 << (j-1))])

    def query_max_left(y1_idx, y2_idx):
        """Get max of left_bounds in range [y1_idx, y2_idx]"""
        if y1_idx > y2_idx:
            y1_idx, y2_idx = y2_idx, y1_idx
        length = y2_idx - y1_idx + 1
        k = int(math.log2(length))
        return max(max_left[k][y1_idx], max_left[k][y2_idx - (1 << k) + 1])

    def query_min_right(y1_idx, y2_idx):
        """Get min of right_bounds in range [y1_idx, y2_idx]"""
        if y1_idx > y2_idx:
            y1_idx, y2_idx = y2_idx, y1_idx
        length = y2_idx - y1_idx + 1
        k = int(math.log2(length))
        return min(min_right[k][y1_idx], min_right[k][y2_idx - (1 << k) + 1])

    def is_valid_rect(x1, y1, x2, y2):
        """Check if rectangle fits entirely within valid region - O(1)"""
        # Get y indices
        if y1 not in y_to_idx or y2 not in y_to_idx:
            return False

        y1_idx = y_to_idx[y1]
        y2_idx = y_to_idx[y2]

        # Get the tightest bounds for this y-range
        max_l = query_max_left(y1_idx, y2_idx)
        min_r = query_min_right(y1_idx, y2_idx)

        # Rectangle x-range must fit within [max_l, min_r]
        min_x = min(x1, x2)
        max_x = max(x1, x2)

        return min_x >= max_l and max_x <= min_r

    print(f"Red tiles: {n}, Unique y-levels: {m}")

    # Check all pairs of red tiles, sorted by area descending
    candidates = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]
            if x1 != x2 and y1 != y2:
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                candidates.append((area, x1, y1, x2, y2))

    candidates.sort(reverse=True)
    print(f"Checking {len(candidates)} candidates...")

    max_area = 0
    for area, x1, y1, x2, y2 in candidates:
        if area <= max_area:
            break
        if is_valid_rect(x1, y1, x2, y2):
            max_area = area

    return max_area

def run_example_part2():
    """Test part 2 with the example from the puzzle"""
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

    print("Example Part 2:")
    result = find_largest_rectangle_with_green(example_coords)
    print(f"Result: {result}")
    print(f"Expected: 24")
    return result == 24

def part2():
    """Solve part 2"""
    input_file = os.path.join(sys.path[0], 'input.txt')
    coords = parse_input(input_file)
    return find_largest_rectangle_with_green(coords)

if __name__ == "__main__":
    # Test with example first
    print("=" * 50)
    print("Testing with example:")
    print("=" * 50)
    run_example()

    print("\n" + "=" * 50)
    print("Testing Part 2 with example:")
    print("=" * 50)
    run_example_part2()

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

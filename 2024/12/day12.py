import os
import sys
from collections import deque

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        return [line.strip() for line in f.readlines()]

def find_regions(grid):
    """Find all regions using flood fill."""
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    regions = []

    def flood_fill(start_r, start_c, plant_type):
        """Flood fill to find all plots in a region."""
        queue = deque([(start_r, start_c)])
        region = []

        while queue:
            r, c = queue.popleft()

            if (r, c) in visited:
                continue

            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue

            if grid[r][c] != plant_type:
                continue

            visited.add((r, c))
            region.append((r, c))

            # Check all 4 neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited:
                    queue.append((nr, nc))

        return region

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                plant_type = grid[r][c]
                region = flood_fill(r, c, plant_type)
                if region:
                    regions.append(region)

    return regions

def calculate_perimeter(region, grid):
    """Calculate the perimeter of a region."""
    rows = len(grid)
    cols = len(grid[0])
    region_set = set(region)
    perimeter = 0

    for r, c in region:
        # Check all 4 sides
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            # If neighbor is outside grid or not in same region, it's a fence side
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or (nr, nc) not in region_set:
                perimeter += 1

    return perimeter

def part1():
    grid = load_input()
    regions = find_regions(grid)

    total_price = 0
    for region in regions:
        area = len(region)
        perimeter = calculate_perimeter(region, grid)
        price = area * perimeter
        total_price += price

    return total_price

def count_corners(region, grid):
    """
    Count the number of corners in a region.
    The number of corners equals the number of sides.

    For each cell, check all 4 possible corner positions:
    - Top-left, top-right, bottom-left, bottom-right

    A corner exists when:
    1. Outer corner: Two adjacent edges are boundaries
    2. Inner corner: Two adjacent edges are inside the region but the diagonal is outside
    """
    region_set = set(region)
    corners = 0

    for r, c in region:
        # Check all 4 corners of this cell
        # For each corner, we need to check 3 positions: the two adjacent cells and the diagonal

        # Top-left corner
        top = (r - 1, c) not in region_set
        left = (r, c - 1) not in region_set
        top_left = (r - 1, c - 1) not in region_set

        # Outer corner: both adjacent sides are boundaries
        if top and left:
            corners += 1
        # Inner corner: both adjacent sides are inside but diagonal is outside
        elif not top and not left and top_left:
            corners += 1

        # Top-right corner
        top = (r - 1, c) not in region_set
        right = (r, c + 1) not in region_set
        top_right = (r - 1, c + 1) not in region_set

        if top and right:
            corners += 1
        elif not top and not right and top_right:
            corners += 1

        # Bottom-left corner
        bottom = (r + 1, c) not in region_set
        left = (r, c - 1) not in region_set
        bottom_left = (r + 1, c - 1) not in region_set

        if bottom and left:
            corners += 1
        elif not bottom and not left and bottom_left:
            corners += 1

        # Bottom-right corner
        bottom = (r + 1, c) not in region_set
        right = (r, c + 1) not in region_set
        bottom_right = (r + 1, c + 1) not in region_set

        if bottom and right:
            corners += 1
        elif not bottom and not right and bottom_right:
            corners += 1

    return corners

def part2():
    grid = load_input()
    regions = find_regions(grid)

    total_price = 0
    for region in regions:
        area = len(region)
        sides = count_corners(region, grid)
        price = area * sides
        total_price += price

    return total_price

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

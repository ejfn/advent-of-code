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

def part2():
    # Part 2 will be implemented after Part 1 is submitted
    pass

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    # print(f"Part 2: {part2()}")

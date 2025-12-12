import os
import sys
from pysat.solvers import Solver as SATSolver
from pysat.card import CardEnc, EncType

def parse_input(data):
    """Parse the input into shapes and regions."""
    sections = data.strip().split('\n\n')

    shapes = []
    regions = []

    for section in sections:
        lines = section.strip().split('\n')
        if lines[0].endswith(':') and 'x' not in lines[0]:
            # This is a shape definition
            shape_lines = lines[1:]
            cells = set()
            for r, line in enumerate(shape_lines):
                for c, ch in enumerate(line):
                    if ch == '#':
                        cells.add((r, c))
            shapes.append(cells)
        else:
            # These are region definitions
            for line in lines:
                if 'x' in line:
                    parts = line.split(':')
                    dims = parts[0].strip()
                    w, h = map(int, dims.split('x'))
                    counts = list(map(int, parts[1].strip().split()))
                    regions.append((w, h, counts))

    return shapes, regions


def normalize(cells):
    """Normalize a shape to start at (0, 0)."""
    if not cells:
        return frozenset()
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return frozenset((r - min_r, c - min_c) for r, c in cells)


def rotate_90(cells):
    """Rotate cells 90 degrees clockwise."""
    return {(c, -r) for r, c in cells}


def flip_h(cells):
    """Flip cells horizontally."""
    return {(r, -c) for r, c in cells}


def get_all_orientations(cells):
    """Get all unique orientations of a shape (rotation + flip)."""
    orientations = set()
    current = cells
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize(flip_h(current)))
        current = rotate_90(current)
    return orientations


def can_fit_region_sat(shapes, width, height, counts):
    """Check if all shapes can fit in the region using SAT solver."""
    # Check total area first
    total_area = sum(len(shapes[idx]) * counts[idx] for idx in range(len(shapes)))
    region_area = width * height
    if total_area > region_area:
        return False

    if sum(counts) == 0:
        return True

    # Get all orientations for each shape
    all_orientations = [get_all_orientations(s) for s in shapes]

    # Get all placements for each shape
    shape_placements = []
    for shape_idx in range(len(shapes)):
        placements = []
        for orient in all_orientations[shape_idx]:
            max_r = max(r for r, c in orient)
            max_c = max(c for r, c in orient)
            for start_r in range(height - max_r):
                for start_c in range(width - max_c):
                    cells = frozenset((r + start_r, c + start_c) for r, c in orient)
                    placements.append(cells)
        shape_placements.append(placements)

    # Create piece instances: (shape_idx, instance_idx)
    pieces = []
    for shape_idx, count in enumerate(counts):
        for inst in range(count):
            pieces.append((shape_idx, inst))

    # SAT variable numbering: start from 1
    # var_id[piece_num][placement_idx] = variable number
    var_counter = [1]

    def new_var():
        v = var_counter[0]
        var_counter[0] += 1
        return v

    # Create variables for each piece-placement
    var_id = []
    for piece_num, (shape_idx, inst) in enumerate(pieces):
        piece_vars = [new_var() for _ in shape_placements[shape_idx]]
        var_id.append(piece_vars)

    solver = SATSolver(name='g4')

    # Each piece must have exactly one placement
    for piece_num, (shape_idx, inst) in enumerate(pieces):
        piece_vars = var_id[piece_num]
        if not piece_vars:
            # No valid placements for this piece
            return False

        # At least one placement (OR of all placements for this piece)
        solver.add_clause(piece_vars)

        # At most one placement (pairwise exclusion)
        for i in range(len(piece_vars)):
            for j in range(i + 1, len(piece_vars)):
                solver.add_clause([-piece_vars[i], -piece_vars[j]])

    # No overlap: for each cell, at most one placement covering it
    cell_to_vars = {}  # cell -> list of variables
    for piece_num, (shape_idx, inst) in enumerate(pieces):
        placements = shape_placements[shape_idx]
        for pl_idx, cells in enumerate(placements):
            var = var_id[piece_num][pl_idx]
            for cell in cells:
                if cell not in cell_to_vars:
                    cell_to_vars[cell] = []
                cell_to_vars[cell].append(var)

    for cell, vars_list in cell_to_vars.items():
        if len(vars_list) > 1:
            # At most one of these can be true
            for i in range(len(vars_list)):
                for j in range(i + 1, len(vars_list)):
                    solver.add_clause([-vars_list[i], -vars_list[j]])

    result = solver.solve()
    solver.delete()
    return result


def can_fit_region_simple(shapes, width, height, counts):
    """Simple area check - returns True if area is sufficient."""
    total_area = sum(len(shapes[idx]) * counts[idx] for idx in range(len(shapes)))
    region_area = width * height
    return total_area <= region_area


def part1(shapes, regions):
    """Count how many regions can fit all their presents."""
    count = 0
    for i, (width, height, shape_counts) in enumerate(regions):
        if can_fit_region_simple(shapes, width, height, shape_counts):
            count += 1
    return count


def run_example():
    """Test with example input."""
    example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

    shapes, regions = parse_input(example)
    print("Shapes parsed:", len(shapes))
    for i, s in enumerate(shapes):
        print(f"  Shape {i}: {len(s)} cells, {s}")
    print("Regions:", regions)

    result = part1(shapes, regions)
    print(f"Example Part 1: {result}")
    assert result == 2, f"Expected 2, got {result}"
    print("Example passed!")


def part2(shapes, regions):
    """Part 2 - TBD"""
    pass


if __name__ == "__main__":
    run_example()

    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read()

    shapes, regions = parse_input(data)
    print(f"\nParsed {len(shapes)} shapes and {len(regions)} regions")

    print("\nRunning Part 1...")
    result1 = part1(shapes, regions)
    print(f"Part 1: {result1}")

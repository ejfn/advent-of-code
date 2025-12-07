import os
import sys
from collections import defaultdict

def parse_input():
    """Parse the input file into rules and updates."""
    with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
        content = f.read().strip()

    # Split on empty line
    parts = content.split('\n\n')
    rules_text = parts[0]
    updates_text = parts[1]

    # Parse rules: X|Y means X must come before Y
    rules = []
    for line in rules_text.split('\n'):
        x, y = line.split('|')
        rules.append((int(x), int(y)))

    # Parse updates
    updates = []
    for line in updates_text.split('\n'):
        update = [int(x) for x in line.split(',')]
        updates.append(update)

    return rules, updates

def is_valid_order(update, rules):
    """Check if an update is in valid order according to rules."""
    # Create a position map for quick lookup
    position = {page: i for i, page in enumerate(update)}

    # Check each rule
    for x, y in rules:
        # Only check if both pages are in this update
        if x in position and y in position:
            # x must come before y
            if position[x] >= position[y]:
                return False

    return True

def part1():
    """Find sum of middle page numbers from correctly-ordered updates."""
    rules, updates = parse_input()

    total = 0
    for update in updates:
        if is_valid_order(update, rules):
            # Find middle page number
            middle_idx = len(update) // 2
            total += update[middle_idx]

    return total

def reorder_update(update, rules):
    """Reorder an update according to the rules using topological sort."""
    # Build a graph of dependencies for pages in this update
    pages = set(update)
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Initialize in_degree for all pages
    for page in pages:
        in_degree[page] = 0

    # Build graph from relevant rules
    for x, y in rules:
        if x in pages and y in pages:
            graph[x].append(y)
            in_degree[y] += 1

    # Topological sort using Kahn's algorithm
    queue = [page for page in pages if in_degree[page] == 0]
    result = []

    while queue:
        # Sort to ensure consistent ordering when there are multiple valid options
        queue.sort()
        node = queue.pop(0)
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result

def part2():
    """Find sum of middle page numbers from corrected incorrectly-ordered updates."""
    rules, updates = parse_input()

    total = 0
    for update in updates:
        if not is_valid_order(update, rules):
            # Reorder this update
            corrected = reorder_update(update, rules)
            # Find middle page number
            middle_idx = len(corrected) // 2
            total += corrected[middle_idx]

    return total

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

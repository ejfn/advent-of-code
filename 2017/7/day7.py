import os
import sys
import re
from collections import Counter


def parse_input(text):
    """Parse input into weights dict and children dict."""
    weights = {}
    children = {}
    
    for line in text.strip().split('\n'):
        match = re.match(r'(\w+) \((\d+)\)(?: -> (.+))?', line)
        if match:
            name, weight, kids = match.groups()
            weights[name] = int(weight)
            if kids:
                children[name] = [k.strip() for k in kids.split(',')]
            else:
                children[name] = []
    
    return weights, children


def part1(weights, children):
    """Find the root program (not a child of any other)."""
    all_programs = set(weights.keys())
    all_children = set()
    for kids in children.values():
        all_children.update(kids)
    
    roots = all_programs - all_children
    return list(roots)[0]


def part2(weights, children):
    """Find the corrected weight for the unbalanced program."""
    # Build total weights (own weight + all descendants)
    total_weight = {}
    
    def calc_total(name):
        if name in total_weight:
            return total_weight[name]
        
        own = weights[name]
        total = own + sum(calc_total(c) for c in children[name])
        total_weight[name] = total
        return total
    
    # Calculate all totals
    root = part1(weights, children)
    calc_total(root)
    
    # Find the unbalanced node
    def find_unbalanced(name, expected_total=None):
        kids = children[name]
        
        if not kids:
            # Leaf node - can't be the problem
            return None
        
        # Get total weights of children
        child_totals = [total_weight[c] for c in kids]
        
        # Check if all children are balanced
        if len(set(child_totals)) == 1:
            # All children balanced - this node is fine
            return None
        
        # Find the odd one out
        counts = Counter(child_totals)
        correct_total = [t for t, c in counts.items() if c > 1][0]
        wrong_total = [t for t, c in counts.items() if c == 1][0]
        
        wrong_child = kids[child_totals.index(wrong_total)]
        
        # Check if the problem is deeper
        result = find_unbalanced(wrong_child, correct_total)
        if result is not None:
            return result
        
        # The problem is this child - calculate corrected weight
        diff = correct_total - wrong_total
        return weights[wrong_child] + diff
    
    return find_unbalanced(root)


def run_example():
    example = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
    weights, children = parse_input(example)
    assert part1(weights, children) == "tknk"
    print("Part 1 example passed!")
    assert part2(weights, children) == 60
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        weights, children = parse_input(f.read())
    
    print(f"Part 1: {part1(weights, children)}")
    print(f"Part 2: {part2(weights, children)}")

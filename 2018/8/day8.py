import sys
import os

sys.setrecursionlimit(20000) # Ensure we have enough depth just in case

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read().strip()
    return list(map(int, content.split()))

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

def parse_tree(data, index):
    # Header: num_children, num_metadata
    num_children = data[index]
    num_metadata = data[index+1]
    index += 2
    
    node = Node()
    
    for _ in range(num_children):
        child, index = parse_tree(data, index)
        node.children.append(child)
        
    for _ in range(num_metadata):
        node.metadata.append(data[index])
        index += 1
        
    return node, index

def sum_metadata(node):
    total = sum(node.metadata)
    for child in node.children:
        total += sum_metadata(child)
    return total

    return total

def get_node_value(node):
    if not node.children:
        return sum(node.metadata)
    
    value = 0
    for m in node.metadata:
        # Metadata values are 1-based indices
        if 1 <= m <= len(node.children):
            value += get_node_value(node.children[m-1])
            
    return value

def solve_part1(data):
    root, _ = parse_tree(data, 0)
    return sum_metadata(root)

def solve_part2(data):
    root, _ = parse_tree(data, 0)
    return get_node_value(root)

def part1():
    data = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part1(data)
    print(f'Part 1: {result}')
    return result

def part2():
    data = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part2(data)
    print(f'Part 2: {result}')
    return result

def run_example():
    print("Running Example...")
    # Example: 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
    example_data = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    result = solve_part1(example_data)
    print(f"Example Part 1 Result: {result}")
    assert result == 138
    
    result2 = solve_part2(example_data)
    print(f"Example Part 2 Result: {result2}")
    assert result2 == 66

if __name__ == '__main__':
    run_example()
    part1()
    part2()

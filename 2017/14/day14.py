import os
import sys
from collections import deque


def knot_hash_round(elements, lengths, pos=0, skip=0):
    """Perform one round of the knot hash algorithm."""
    n = len(elements)
    
    for length in lengths:
        indices = [(pos + i) % n for i in range(length)]
        values = [elements[i] for i in indices]
        values.reverse()
        for i, idx in enumerate(indices):
            elements[idx] = values[i]
        
        pos = (pos + length + skip) % n
        skip += 1
    
    return pos, skip


def knot_hash(input_str):
    """Full knot hash producing hex string."""
    lengths = [ord(c) for c in input_str.strip()] + [17, 31, 73, 47, 23]
    
    elements = list(range(256))
    pos, skip = 0, 0
    
    for _ in range(64):
        pos, skip = knot_hash_round(elements, lengths, pos, skip)
    
    dense = []
    for i in range(16):
        block = elements[i*16:(i+1)*16]
        xor = 0
        for v in block:
            xor ^= v
        dense.append(xor)
    
    return ''.join(f'{x:02x}' for x in dense)


def hex_to_binary(hex_str):
    """Convert hex string to binary string."""
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)


def build_grid(key):
    """Build 128x128 grid from key using knot hashes."""
    grid = []
    for row in range(128):
        hash_input = f"{key}-{row}"
        hash_result = knot_hash(hash_input)
        binary = hex_to_binary(hash_result)
        grid.append(binary)
    return grid


def part1(key):
    """Count used squares in the grid."""
    grid = build_grid(key)
    return sum(row.count('1') for row in grid)


def part2(key):
    """Count connected regions in the grid."""
    grid = build_grid(key)
    visited = set()
    regions = 0
    
    def bfs(start_r, start_c):
        queue = deque([(start_r, start_c)])
        while queue:
            r, c = queue.popleft()
            if (r, c) in visited:
                continue
            if r < 0 or r >= 128 or c < 0 or c >= 128:
                continue
            if grid[r][c] != '1':
                continue
            visited.add((r, c))
            queue.extend([(r-1, c), (r+1, c), (r, c-1), (r, c+1)])
    
    for r in range(128):
        for c in range(128):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs(r, c)
                regions += 1
    
    return regions


def run_example():
    assert part1("flqrgnkx") == 8108
    print("Part 1 example passed!")
    assert part2("flqrgnkx") == 1242
    print("Part 2 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        key = f.read().strip()
    
    print(f"Part 1: {part1(key)}")
    print(f"Part 2: {part2(key)}")

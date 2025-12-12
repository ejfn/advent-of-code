import os
import sys


def knot_hash_round(elements, lengths, pos=0, skip=0):
    """Perform one round of the knot hash algorithm."""
    n = len(elements)
    
    for length in lengths:
        # Reverse 'length' elements starting at 'pos'
        indices = [(pos + i) % n for i in range(length)]
        values = [elements[i] for i in indices]
        values.reverse()
        for i, idx in enumerate(indices):
            elements[idx] = values[i]
        
        pos = (pos + length + skip) % n
        skip += 1
    
    return pos, skip


def part1(lengths_str, size=256):
    """Simple knot hash - multiply first two elements after one round."""
    lengths = [int(x) for x in lengths_str.split(',')]
    elements = list(range(size))
    knot_hash_round(elements, lengths)
    return elements[0] * elements[1]


def knot_hash(input_str):
    """Full knot hash producing hex string."""
    # Convert to ASCII codes and add suffix
    lengths = [ord(c) for c in input_str.strip()] + [17, 31, 73, 47, 23]
    
    elements = list(range(256))
    pos, skip = 0, 0
    
    # 64 rounds
    for _ in range(64):
        pos, skip = knot_hash_round(elements, lengths, pos, skip)
    
    # Dense hash: XOR each block of 16
    dense = []
    for i in range(16):
        block = elements[i*16:(i+1)*16]
        xor = 0
        for v in block:
            xor ^= v
        dense.append(xor)
    
    # Convert to hex
    return ''.join(f'{x:02x}' for x in dense)


def part2(input_str):
    return knot_hash(input_str)


def run_example():
    # Part 1 example with size 5
    lengths_str = "3,4,1,5"
    lengths = [int(x) for x in lengths_str.split(',')]
    elements = list(range(5))
    knot_hash_round(elements, lengths)
    assert elements[0] * elements[1] == 12
    print("Part 1 example passed!")
    
    # Part 2 examples
    assert part2("") == "a2582a3a0e66e6e86e3812dcb672a272"
    assert part2("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
    assert part2("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
    assert part2("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"
    print("Part 2 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        input_str = f.read().strip()
    
    print(f"Part 1: {part1(input_str)}")
    print(f"Part 2: {part2(input_str)}")

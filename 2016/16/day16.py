import sys
import os

def generate_dragon_curve(a):
    b = a[::-1]
    # In b, replace 0->1 and 1->0
    # efficient way: translate
    # '0' is ord 48, '1' is ord 49
    trans_table = str.maketrans({'0': '1', '1': '0'})
    b = b.translate(trans_table)
    return a + '0' + b

def fill_disk(initial_state, target_length):
    data = initial_state
    while len(data) < target_length:
        data = generate_dragon_curve(data)
    return data[:target_length]

def calculate_checksum(data):
    checksum = data
    while len(checksum) % 2 == 0:
        # Process pairs
        # Efficient way using list comprehension or zip
        # 00 -> 1, 11 -> 1, 01 -> 0, 10 -> 0
        # Same -> 1, Diff -> 0
        # If we map '0'->0, '1'->1
        # same: (x+y)%2 == 0? No. '0'==0, '1'==1.
        # '00': 0+0=0 (same) -> 1
        # '11': 1+1=2 (same) -> 1
        # '01': 0+1=1 (diff) -> 0
        # '10': 1+0=1 (diff) -> 0
        # So same is 1, diff is 0.
        
        # Generator expression might be slower than building list in chunks?
        # Let's try simple iteration
        
        # Optimization: String operations in Python are quite optimized.
        # But constructing massive strings repeatedly might be slow for Part 2 (35MB).
        # However, checksum reduces length by half each time.
        # 35MB -> 17MB -> 8MB -> 4MB...
        # It's fast enough.
        
        pairs = zip(checksum[::2], checksum[1::2])
        new_checksum = []
        for a, b in pairs:
            if a == b:
                new_checksum.append('1')
            else:
                new_checksum.append('0')
        checksum = "".join(new_checksum)
        
    return checksum

def solve(initial_state, length):
    data = fill_disk(initial_state, length)
    return calculate_checksum(data)

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        initial_state = f.read().strip()
    return solve(initial_state, 272)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        initial_state = f.read().strip()
    return solve(initial_state, 35651584)

def run_example():
    # Example: 10000 -> len 20 -> checksum 01100
    state = "10000"
    length = 20
    result = solve(state, length)
    print(f"Example result: {result} (expected 01100)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

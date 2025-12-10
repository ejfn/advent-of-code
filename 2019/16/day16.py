
import sys
import os
import math

def parse_input(data):
    return [int(x) for x in data.strip()]

def get_pattern(index, length):
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for val in base_pattern:
        pattern.extend([val] * (index + 1))
    
    # We need to shift left by 1 (skip first element)
    # And then cycle
    
    # Actually, generating the full pattern is slow for large length.
    # But for Part 1 (length ~650, 100 phases), it's fine (650^2 * 100 operations).
    pass

def solve_part1(data):
    signal = parse_input(data)
    n = len(signal)
    
    for phase in range(100):
        new_signal = []
        for i in range(n):
            pattern_val_idx = 1 # Skip first one
            val = 0
            
            # Pattern repeats: 0*i+1, 1*i+1, 0*i+1, -1*i+1
            # We can write a generator or just loop
            
            # Optimization: 
            # Pattern is [0]*(i+1) + [1]*(i+1) + [0]*(i+1) + [-1]*(i+1)
            # repeating.
            # We skip the very first element of the very first block.
            
            # Let's do it simply first
            base_pattern = [0, 1, 0, -1]
            repeat_len = i + 1
            
            # Constructing pattern is costly if done naively every time. 
            # But n is small (650).
            
            current_sum = 0
            for j in range(n):
                # pattern index: (j + 1) // repeat_len % 4
                # +1 because we skip the first element of the theoretical pattern
                p_idx = ((j + 1) // repeat_len) % 4
                current_sum += signal[j] * base_pattern[p_idx]
                
            new_signal.append(abs(current_sum) % 10)
        signal = new_signal
        
    return ''.join(map(str, signal[:8]))

def solve_part2(data):
    # Real input is multiplied by 10000. Length ~ 6.5 million.
    # 100 phases.
    # O(N^2) is impossible.
    # Look at the pattern for the second half of the signal.
    # Pattern for index i:
    # 0 for j < i
    # 1 for i <= j < 2i+1 (usually just until end if i >= N/2)
    # ...
    
    # If offset (message offset) is in the second half of the signal (offset >= length / 2):
    # For any output element i >= offset:
    # Pattern is 0 for j < i
    # Pattern is 1 for j >= i (since N < 2*i+1 usually means 1s go till end)
    # So new_signal[i] = sum(signal[i:]) % 10
    
    # This means new_signal[N-1] = signal[N-1] % 10
    # new_signal[N-2] = (signal[N-2] + signal[N-1]) % 10 = (signal[N-2] + new_signal[N-1]) % 10
    # Generally: new_signal[i] = (signal[i] + new_signal[i+1]) % 10
    
    # So we can compute from the end backwards!
    
    raw_input = parse_input(data)
    offset = int(data[:7])
    
    full_len = len(raw_input) * 10000
    
    if offset < full_len // 2:
        print("Warning: Offset is in first half, optimization trick won't work")
    
    # We only care about signal from offset to end
    # Construct that part of the signal
    current_signal = (raw_input * 10000)[offset:]
    
    for phase in range(100):
        # Calculate suffix sums modulo 10
        # new[i] = (current[i] + new[i+1]) % 10
        # Running sum from back
        running_sum = 0
        for i in range(len(current_signal) - 1, -1, -1):
            running_sum = (running_sum + current_signal[i]) % 10
            current_signal[i] = running_sum
            
    return ''.join(map(str, current_signal[:8]))

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))

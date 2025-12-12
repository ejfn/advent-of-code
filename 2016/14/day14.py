import sys
import os
import hashlib
import re
from collections import deque

class KeyFinder:
    def __init__(self, salt, stretch=0):
        self.salt = salt
        self.stretch = stretch
        self.hash_cache = {}
        # Optimization: Pre-scan cache for quintuplets?
        # Actually simple memoization is fine for N=64 keys.
        # We might need to go up to index 25000 approx.
        # 25000 hashes is fast for regular MD5. 
        # For stretched MD5 (2016 extra hashes), it's 25000 * 2017 hashes ~ 50 million hashes.
        # That takes a while in Python (maybe 20-30s). Acceptable.

    def get_hash(self, index):
        if index in self.hash_cache:
            return self.hash_cache[index]
        
        # Calculate
        h = hashlib.md5(f"{self.salt}{index}".encode('utf-8')).hexdigest()
        for _ in range(self.stretch):
            h = hashlib.md5(h.encode('utf-8')).hexdigest()
            
        self.hash_cache[index] = h
        return h

    def find_triplet(self, h):
        # "contains three of the same character in a row... Only consider the first such triplet"
        # We can scan the string.
        for i in range(len(h) - 2):
            if h[i] == h[i+1] == h[i+2]:
                return h[i]
        return None

    def has_quintuplet(self, h, char):
        target = char * 5
        return target in h

    def solve(self, n_keys=64):
        keys = []
        i = 0
        while len(keys) < n_keys:
            h = self.get_hash(i)
            char = self.find_triplet(h)
            
            if char:
                # Check next 1000
                is_key = False
                for j in range(1, 1001):
                    h_next = self.get_hash(i + j)
                    if self.has_quintuplet(h_next, char):
                        is_key = True
                        break
                
                if is_key:
                    keys.append(i)
                    # print(f"Key {len(keys)} found at index {i}")
            
            i += 1
            
        return keys[-1]

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        salt = f.read().strip()
    
    finder = KeyFinder(salt)
    return finder.solve(64)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        salt = f.read().strip()
    
    finder = KeyFinder(salt, stretch=2016)
    return finder.solve(64)

def run_example():
    print("Running example with salt 'abc'...")
    finder = KeyFinder("abc")
    # First key should be 39
    # 64th key should be 22728
    
    # Let's verify a few keys
    keys = []
    i = 0
    print("Finding first key...")
    while len(keys) < 1:
        h = finder.get_hash(i)
        char = finder.find_triplet(h)
        if char:
            is_key = False
            for j in range(1, 1001):
                if finder.has_quintuplet(finder.get_hash(i+j), char):
                    is_key = True
                    break
            if is_key:
                keys.append(i)
                print(f"Key {len(keys)}: {i}")
        i += 1
        
    if keys[0] == 39:
        print("First key match verified!")
    else:
        print(f"Mismatch: Expected 39, got {keys[0]}")
        
    # We won't run to 64 in example unless requested, it might take a bit.
    # The example says "Eventually, index 22728 meets all of the criteria".
    # We can rely on Part 1 test for full run.

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

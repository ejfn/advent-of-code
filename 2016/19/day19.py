import sys
import os
import math
from collections import deque

def solve_part1(n):
    # Josephus Problem k=2
    # n = 2^m + l
    # Winner = 2*l + 1
    # Find highest power of 2 less than or equal to n
    if n < 1:
        return 0
    m = int(math.log2(n))
    l = n - (2 ** m)
    return 2 * l + 1

def solve_part2_simulation(n):
    # Simulation using two deques for O(N)
    # Removing from across the circle:
    # Target index is floor(len/2) steps away.
    
    # Left side: 1 ... n//2
    # Right side: n//2 + 1 ... n
    
    left = deque()
    right = deque()
    
    for i in range(1, (n // 2) + 1):
        left.append(i)
    for i in range((n // 2) + 1, n + 1):
        right.append(i)
        
    while left and right:
        # Total elves remaining
        total = len(left) + len(right)
        if total == 1:
            break
            
        # Target to remove is floor(total / 2) steps away.
        # Current elf is at left[0] (but we process by rotating).
        # We assume the "current" elf is conceptually just acted, and moves to back.
        # But wait, the structure is:
        # Elves 1..N arranged in circle.
        # Current elf is 1. Target is across.
        # After stealing, current elf is next (2).
        
        # With two deques splitting the circle:
        # L: [1, 2, ..., k]
        # R: [k+1, ..., n]
        # Current is L[0].
        # Target is roughly R[0] if sizes balanced.
        
        # Balance invariant: len(left) == len(right) or len(left) == len(right) + 1?
        # Target index from current is total // 2.
        # If len(left) ~ len(right), then target is in right side or end of left?
        # Let's trace N=5. 1 2 3 4 5.
        # L: [1, 2] R: [3, 4, 5]
        # Current 1. Target is (floor(5/2) = 2) steps away: 1 -> 2 -> 3. Target is 3. 3 is R[0].
        # Remove R[0].
        # R becomes [4, 5]. L is [1, 2].
        # Rotate: Current becomes 2. 2 is L[1], now L[0].
        # 1 goes to back of ... where? Order is L then R.
        # 1 goes to end of R? No, back of queue.
        # Better: keep 'current' always at start of L (or R?).
        # Rotation: Pop L[0], append to R. Pop R[0], append to L?
        
        # Let's maintain 'current' implied by always rotating.
        # Actually simpler logic:
        # If sizes are equal, target is R[0]. (dist = size)
        # If len(L) < len(R): target is R[0]. (dist > len(L))
        # Wait, let's just use the property:
        # If we maintain len(left) == len(right) or len(left) == len(right) + 1.
        # Target is always "across".
        
        # If total=5. L: [1, 2], R: [3, 4, 5].
        # Target is 3 (R[0]). Remove R[0].
        # L: [1, 2], R: [4, 5].
        # Next turn: Current is 2.
        # We rotate 1 to back of R? 
        # State: 1 (done), 2 (current), ...
        # Effectively: Move L[0] to R end.
        # L: [2], R: [4, 5, 1].
        # Rebalance: L should be ~half.
        # L: [2, 4], R: [5, 1].
        # Target for 2 (total 4, dist 2): 2 -> 4 -> 5. 5 is R[0].
        # Remove R[0].
        
        # Algorithm:
        # 1. If len(left) > len(right): pop left[-1]? No.
        # Let's strictly follow:
        # Target is at index `floor(len / 2)` from current `0`.
        # If we keep `current` at `left[0]`.
        # index `k = len // 2`.
        # If `k < len(left)`: target is in left.
        # If `k >= len(left)`: target is in right at `k - len(left)`.
        
        # Rebalancing ensures target is always at specific spot?
        # If we keep `len(left)` equal to `len(right)` or `len(left) == len(right) + 1`.
        # Total `N`. `floor(N/2)` is the distance.
        # If `N` even: `N/2` in R.
        # If `N` odd: `(N-1)/2` in R?
        
        # Example N=5. `5//2 = 2`.
        # L: [1, 2, 3] R: [4, 5]. (Size 3, 2).
        # Target is `left[0 + 2] = 3`? 
        # If we index 0..N-1: 0, 1, 2.
        # Target is `(0 + 2) % 5 = 2`. Index 2 is in L (if L has 3).
        # 3 is removed. L: [1, 2], R: [4, 5].
        # Rotate: 1 moves to back.
        # L: [2, 4], R: [5, 1]. (Size 2, 2).
        # Total 4. `4//2 = 2`.
        # Target `(0 + 2) = 2`. L has 2. Target in R[0] (Index 2).
        # R[0] is 5. Remove 5.
        # L: [2, 4], R: [1].
        # Rotate: 2 moves to back.
        # L: [4, 1], R: [2]? No, rebalance.
        # L: [4, 1], R: [2]. (Size 2, 1).
        # Total 3. `3//2 = 1`.
        # Target `1`. L[1] is 1. Remove 1.
        # L: [4], R: [2].
        # Rotate: 4 moves.
        # L: [2], R: [4].
        # Total 2. `2//2 = 1`. Target R[0] (4). Remove 4.
        # L: [2], R: [].
        # Winner 2.
        
        # Let's refine the loop with rebalance.
        if len(left) > len(right):
            left.pop() # The element at the "end" of left is the across element if sizes are imbalanced? 
            # Wait, let's look at logic:
            # If size=5 (3, 2). Target index 2 (0-indexed). L[2] is target. L[2] is last of L.
            # So pop L[-1].
        else:
            right.popleft() # Target index is R[0].
            
        # Rotate current (L[0]) to back of R
        # And ensure L takes from R
        
        # Actually simpler rotation:
        # Move head of L to tail of R? No, tail of R is far side.
        # Logical order: L[0]...L[-1] R[0]...R[-1].
        # Current is L[0].
        # Move L[0] to R (become valid tail).
        # Move R[0] to L (become valid tail of L side).
        
        right.append(left.popleft())
        
        # Rebalance:
        # We want len(left) == len(right) or len(left) == len(right) + 1.
        # Current: L lost 1, R gained 1. R might be too big.
        if len(right) > len(left):
            left.append(right.popleft())
            
    return left[0]

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        # Input is a single number
        n = int(f.read().strip())
    return solve_part1(n)

def part2():
    # To be implemented properly after verification or trigger
    # But since I have a generalized Plan, I can implement it but return None until asked?
    # Or just return it.
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        n = int(f.read().strip())
    return solve_part2_simulation(n)

def run_example():
    # Ex: 5 elves. Part 1 Winner 3. Part 2 Winner 2.
    print(f"Part 1 Example (5): {solve_part1(5)} (Expected 3)")
    print(f"Part 2 Example (5): {solve_part2_simulation(5)} (Expected 2)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

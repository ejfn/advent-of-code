import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from day25 import parse_input, fits

def test_example():
    locks, keys = parse_input(os.path.join(sys.path[0], 'test_input.txt'))

    print(f"Locks: {locks}")
    print(f"Keys: {keys}")

    # Expected from puzzle:
    # Locks: (0,5,3,4,3), (1,2,0,5,3)
    # Keys: (5,0,2,1,3), (4,3,4,0,2), (3,0,2,0,1)

    count = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                print(f"Lock {lock} fits key {key}")
                count += 1

    print(f"\nTotal fitting pairs: {count}")
    print(f"Expected: 3")

if __name__ == "__main__":
    test_example()

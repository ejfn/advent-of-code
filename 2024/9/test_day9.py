import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from day9 import parse_disk_map, compact_disk, calculate_checksum

# Test with example
disk_map = "2333133121414131402"
blocks = parse_disk_map(disk_map)

# Print initial state
print("Initial blocks:")
print(''.join(str(b) if b is not None else '.' for b in blocks))

# Compact
compacted = compact_disk(blocks)

# Print compacted state
print("\nCompacted blocks:")
print(''.join(str(b) if b is not None else '.' for b in compacted))

# Calculate checksum
checksum = calculate_checksum(compacted)
print(f"\nChecksum: {checksum}")
print(f"Expected: 1928")

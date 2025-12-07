import os
import sys

def parse_disk_map(disk_map):
    """Parse disk map into a list of blocks where each block is either a file ID or None (free space)"""
    blocks = []
    file_id = 0

    for i, length in enumerate(disk_map):
        length = int(length)
        if i % 2 == 0:  # File
            blocks.extend([file_id] * length)
            file_id += 1
        else:  # Free space
            blocks.extend([None] * length)

    return blocks

def compact_disk(blocks):
    """Move file blocks from the end to leftmost free space"""
    blocks = blocks.copy()  # Don't modify original

    while True:
        # Find leftmost free space
        try:
            free_idx = blocks.index(None)
        except ValueError:
            # No free space left
            break

        # Find rightmost file block
        last_file_idx = None
        for i in range(len(blocks) - 1, -1, -1):
            if blocks[i] is not None:
                last_file_idx = i
                break

        # If no file blocks or all file blocks are before free space, we're done
        if last_file_idx is None or last_file_idx < free_idx:
            break

        # Move the file block
        blocks[free_idx] = blocks[last_file_idx]
        blocks[last_file_idx] = None

    return blocks

def calculate_checksum(blocks):
    """Calculate filesystem checksum"""
    checksum = 0
    for position, file_id in enumerate(blocks):
        if file_id is not None:
            checksum += position * file_id
    return checksum

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        disk_map = f.read().strip()

    blocks = parse_disk_map(disk_map)
    compacted = compact_disk(blocks)
    checksum = calculate_checksum(compacted)

    return checksum

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        disk_map = f.read().strip()

    # TODO: Implement part 2
    return 0

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

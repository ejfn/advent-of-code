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

def compact_disk_whole_files(blocks):
    """Move whole files to leftmost contiguous free space, in order of decreasing file ID"""
    blocks = blocks.copy()  # Don't modify original

    # Find all files (their positions and lengths)
    max_file_id = max(b for b in blocks if b is not None)

    # Process files in decreasing order of file ID
    for file_id in range(max_file_id, -1, -1):
        # Find all positions of this file
        file_positions = [i for i, b in enumerate(blocks) if b == file_id]
        if not file_positions:
            continue

        file_start = file_positions[0]
        file_length = len(file_positions)

        # Find leftmost contiguous free space that can fit this file
        best_pos = None
        i = 0
        while i < file_start:  # Only consider positions to the left of the file
            if blocks[i] is None:
                # Found start of free space, check if it's big enough
                free_start = i
                free_length = 0
                while i < len(blocks) and blocks[i] is None:
                    free_length += 1
                    i += 1

                if free_length >= file_length:
                    best_pos = free_start
                    break
            else:
                i += 1

        # If we found a suitable position, move the file
        if best_pos is not None:
            # Clear old positions
            for pos in file_positions:
                blocks[pos] = None
            # Write to new positions
            for j in range(file_length):
                blocks[best_pos + j] = file_id

    return blocks

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path, 'r') as f:
        disk_map = f.read().strip()

    blocks = parse_disk_map(disk_map)
    compacted = compact_disk_whole_files(blocks)
    checksum = calculate_checksum(compacted)

    return checksum

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

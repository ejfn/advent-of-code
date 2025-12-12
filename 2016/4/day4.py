import os
import sys
from collections import Counter

def parse_room(line):
    """Parse a room line into name, sector_id, and checksum."""
    # Split by '[' to get checksum
    parts = line.strip().split('[')
    checksum = parts[1].rstrip(']')
    
    # Split the rest by '-' to get name parts and sector ID
    name_and_id = parts[0].split('-')
    sector_id = int(name_and_id[-1])
    name_parts = name_and_id[:-1]
    name = '-'.join(name_parts)
    
    return name, sector_id, checksum

def is_real_room(name, checksum):
    """Check if a room is real by validating its checksum."""
    # Count letters (excluding dashes)
    letter_counts = Counter(name.replace('-', ''))
    
    # Sort by count (descending) then alphabetically
    sorted_letters = sorted(letter_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Get the five most common letters
    expected_checksum = ''.join([letter for letter, _ in sorted_letters[:5]])
    
    return expected_checksum == checksum

def part1():
    """Solve part 1."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    
    total = 0
    for line in lines:
        if not line.strip():
            continue
        name, sector_id, checksum = parse_room(line)
        if is_real_room(name, checksum):
            total += sector_id
    
    return total

def decrypt_name(name, sector_id):
    """Decrypt the room name using shift cipher."""
    decrypted = []
    for char in name:
        if char == '-':
            decrypted.append(' ')
        else:
            # 'a' is 97
            # 0-25 + sector_id % 26
            shift = sector_id % 26
            new_ord = ord(char) + shift
            if new_ord > ord('z'):
                new_ord -= 26
            decrypted.append(chr(new_ord))
    return "".join(decrypted)

def part2():
    """Solve part 2."""
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = f.readlines()
    
    for line in lines:
        if not line.strip():
            continue
        name, sector_id, checksum = parse_room(line)
        if is_real_room(name, checksum):
            real_name = decrypt_name(name, sector_id)
            if "north" in real_name and "pole" in real_name:
                print(f"Found it: {real_name} -> {sector_id}")
                return sector_id
    
    return None

def run_example():
    """Test with example data."""
    examples = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-f-g-h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]"
    ]
    
    total = 0
    for line in examples:
        name, sector_id, checksum = parse_room(line)
        is_real = is_real_room(name, checksum)
        print(f"{line}: {is_real}")
        if is_real:
            total += sector_id
    
    print(f"Total: {total} (expected 1514)")
    
    # Part 2 example
    ex2 = "qzmt-zixmtkozy-ivhz-343"
    # parse manually roughly as it doesn't have checksum
    name = "qzmt-zixmtkozy-ivhz"
    sid = 343
    print(f"Decrypt example: {decrypt_name(name, sid)}")

if __name__ == "__main__":
    print("Testing examples:")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())

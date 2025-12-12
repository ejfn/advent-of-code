import hashlib
import sys
import os

def solve_part1(door_id):
    print(f"Crack password for: {door_id}")
    password = []
    i = 0
    while len(password) < 8:
        to_hash = f"{door_id}{i}".encode('utf-8')
        digest = hashlib.md5(to_hash).hexdigest()
        if digest.startswith("00000"):
            char = digest[5]
            password.append(char)
            print(f"Found char: {char} at index {i} (pass so far: {''.join(password)})")
        i += 1
    return "".join(password)

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        door_id = f.read().strip()
    return solve_part1(door_id)

def solve_part2(door_id):
    print(f"Crack password Part 2 for: {door_id}")
    password = [None] * 8
    items_found = 0
    i = 0
    while items_found < 8:
        to_hash = f"{door_id}{i}".encode('utf-8')
        digest = hashlib.md5(to_hash).hexdigest()
        if digest.startswith("00000"):
            pos_char = digest[5]
            val_char = digest[6]
            if pos_char.isdigit():
                pos = int(pos_char)
                if 0 <= pos <= 7 and password[pos] is None:
                    password[pos] = val_char
                    items_found += 1
                    current_pass = "".join([c if c else "_" for c in password])
                    print(f"Found pos {pos}: {val_char} at index {i} (pass so far: {current_pass})")
        i += 1
    return "".join(password)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        door_id = f.read().strip()
    return solve_part2(door_id)

def run_example():
    door_id = "abc"
    result = solve_part1(door_id)
    print(f"Example result: {result} (expected 18f47a30)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_example()
    else:
        print("Part 1:", part1())
        print("Part 2:", part2())

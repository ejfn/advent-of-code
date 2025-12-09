
import os
import sys

def check_valid(num):
    s = str(num)
    if len(s) != 6: return False
    
    has_double = False
    for i in range(len(s) - 1):
        if s[i] == s[i+1]:
            has_double = True
        if s[i] > s[i+1]:
            return False
            
    return has_double

def part1(data):
    start, end = map(int, data.split('-'))
    count = 0
    for num in range(start, end + 1):
        if check_valid(num):
            count += 1
    return count


def check_valid_p2(num):
    s = str(num)
    if len(s) != 6: return False
    
    # Check increasing
    for i in range(len(s) - 1):
        if s[i] > s[i+1]:
            return False
            
    # Check group lengths
    groups = []
    current_char = s[0]
    current_len = 1
    for i in range(1, len(s)):
        if s[i] == current_char:
            current_len += 1
        else:
            groups.append(current_len)
            current_char = s[i]
            current_len = 1
    groups.append(current_len)
    
    return 2 in groups

def part2(data):
    start, end = map(int, data.split('-'))
    count = 0
    for num in range(start, end + 1):
        if check_valid_p2(num):
            count += 1
    return count

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read().strip()
    
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")

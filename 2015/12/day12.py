import os
import sys
import re
import json

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def part1(data):
    numbers = re.findall(r'-?\d+', data)
    return sum(int(n) for n in numbers)

def sum_without_red(obj):
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return 0
    elif isinstance(obj, list):
        return sum(sum_without_red(item) for item in obj)
    elif isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        return sum(sum_without_red(v) for v in obj.values())
    return 0

def part2(data):
    obj = json.loads(data)
    return sum_without_red(obj)

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

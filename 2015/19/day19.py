import os
import sys
import re
from random import shuffle

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return f.read().strip()

def parse_input(data):
    parts = data.split('\n\n')
    replacements = []
    for line in parts[0].split('\n'):
        src, dst = line.split(' => ')
        replacements.append((src, dst))
    molecule = parts[1]
    return replacements, molecule

def part1(data):
    replacements, molecule = parse_input(data)
    results = set()
    for src, dst in replacements:
        for m in re.finditer(src, molecule):
            new_mol = molecule[:m.start()] + dst + molecule[m.end():]
            results.add(new_mol)
    return len(results)

def part2(data):
    replacements, molecule = parse_input(data)
    # Reverse the replacements to work backwards from molecule to 'e'
    target = molecule
    count = 0
    
    while target != 'e':
        found = False
        for src, dst in replacements:
            if dst in target:
                # Replace one occurrence
                idx = target.find(dst)
                target = target[:idx] + src + target[idx + len(dst):]
                count += 1
                found = True
                break
        if not found:
            # Restart with shuffled replacements
            target = molecule
            count = 0
            shuffle(replacements)
    
    return count

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

import os
import sys
from collections import Counter

def load_input(filename):
    """Load box IDs from input file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def part1(boxes):
    """Compute checksum: (# with exactly 2) * (# with exactly 3)."""
    twos = threes = 0
    for box in boxes:
        counts = Counter(box)
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    return twos * threes

def part2(boxes):
    """Find two boxes differing by exactly one letter, return common letters."""
    n = len(boxes)
    for i in range(n):
        for j in range(i + 1, n):
            common_letters = []
            diff_count = 0
            for k in range(len(boxes[i])):
                if boxes[i][k] == boxes[j][k]:
                    common_letters.append(boxes[i][k])
                else:
                    diff_count += 1
                    if diff_count > 1:
                        break
            if diff_count == 1:
                return ''.join(common_letters)
    raise ValueError("No matching pair found")

def run_examples():
    """Run examples from puzzle."""
    # Part 1 illustrative examples (checksum for some input is 12)
    p1_example = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee""".strip().splitlines()
    print("Part 1 example boxes checksum:", part1(p1_example))
    print("(Puzzle example input checksum: 12)")
    
    # Part 2 example
    p2_example = """abcde
fghij
abcde
fguij
axcye
wvxyz""".strip().splitlines()
    print("Part 2 example common letters:", part2(p2_example))
    print("(Expected: fgij)")

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    try:
        boxes = load_input(input_path)
        print("Part 1:", part1(boxes))
        print("Part 2:", part2(boxes))
    except FileNotFoundError:
        print("input.txt not found. Running examples:")
        run_examples()
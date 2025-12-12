import os
import sys


def solve(stream):
    """Returns (total score, garbage char count)."""
    score = 0
    garbage_count = 0
    depth = 0
    in_garbage = False
    i = 0
    
    while i < len(stream):
        char = stream[i]
        
        if in_garbage:
            if char == '!':
                i += 1  # Skip next char
            elif char == '>':
                in_garbage = False
            else:
                garbage_count += 1
        else:
            if char == '{':
                depth += 1
            elif char == '}':
                score += depth
                depth -= 1
            elif char == '<':
                in_garbage = True
        
        i += 1
    
    return score, garbage_count


def part1(stream):
    return solve(stream)[0]


def part2(stream):
    return solve(stream)[1]


def run_example():
    # Part 1 examples
    assert part1("{}") == 1
    assert part1("{{{}}}") == 6
    assert part1("{{},{}}") == 5
    assert part1("{{{},{},{{}}}}") == 16
    assert part1("{<a>,<a>,<a>,<a>}") == 1
    assert part1("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
    assert part1("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
    assert part1("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3
    print("Part 1 examples passed!")
    
    # Part 2 examples
    assert part2("<>") == 0
    assert part2("<random characters>") == 17
    assert part2("<<<<>") == 3
    assert part2("<{!>}>") == 2
    assert part2("<!!>") == 0
    assert part2("<!!!>>") == 0
    assert part2('<{o"i!a,<{i<a>') == 10
    print("Part 2 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        stream = f.read().strip()
    
    print(f"Part 1: {part1(stream)}")
    print(f"Part 2: {part2(stream)}")

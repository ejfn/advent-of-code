import os
import sys


def part1(passphrases):
    """Count passphrases with no duplicate words."""
    valid = 0
    for pp in passphrases:
        words = pp.split()
        if len(words) == len(set(words)):
            valid += 1
    return valid


def part2(passphrases):
    """Count passphrases with no anagram words."""
    valid = 0
    for pp in passphrases:
        words = pp.split()
        sorted_words = [''.join(sorted(w)) for w in words]
        if len(sorted_words) == len(set(sorted_words)):
            valid += 1
    return valid


def run_example():
    # Part 1 examples
    assert part1(["aa bb cc dd ee"]) == 1
    assert part1(["aa bb cc dd aa"]) == 0
    assert part1(["aa bb cc dd aaa"]) == 1
    print("Part 1 examples passed!")
    
    # Part 2 examples
    assert part2(["abcde fghij"]) == 1
    assert part2(["abcde xyz ecdab"]) == 0
    assert part2(["a ab abc abd abf abj"]) == 1
    assert part2(["iiii oiii ooii oooi oooo"]) == 1
    assert part2(["oiii ioii iioi iiio"]) == 0
    print("Part 2 examples passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        passphrases = [line.strip() for line in f if line.strip()]
    
    print(f"Part 1: {part1(passphrases)}")
    print(f"Part 2: {part2(passphrases)}")

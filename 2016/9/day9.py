import sys
import os
import re

def decompressed_length(s):
    length = 0
    i = 0
    while i < len(s):
        if s[i] == '(':
            # Find end of marker
            try:
                end_marker = s.find(')', i)
                if end_marker == -1:
                    # just text? shouldn't happen based on spec
                    length += 1
                    i += 1
                    continue
                
                marker = s[i+1:end_marker]
                # parse AxB
                parts = marker.split('x')
                if len(parts) != 2:
                     # not a marker
                    length += 1
                    i += 1
                    continue
                    
                chars_to_take = int(parts[0])
                repeat_count = int(parts[1])
                
                # Check bounds
                if end_marker + 1 + chars_to_take > len(s):
                    # incomplete data for marker? treat as text or invalid?
                    # Spec says "take the subsequent 10 characters".
                    # We assume valid input.
                    pass
                
                length += chars_to_take * repeat_count
                i = end_marker + 1 + chars_to_take
            except ValueError:
                # parsing int failed, not a marker
                length += 1
                i += 1
        else:
            length += 1
            i += 1
            
    return length

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read().strip() # remove newline at EOF
    # Remove all whitespace as per "Whitespace is ignored"?
    # "The format compresses a sequence of characters. Whitespace is ignored."
    # BUT "ADVENT contains no markers...".
    # Usually AoC whitespace ignored means ignore traversing newlines, but the input is single line.
    # Actually, input might have newlines?
    # View file showed 2 lines, line 1 is long, line 2 empty.
    # Let's strip whitespace just in case.
    # "Whitespace is ignored" usually implies we should strip it before processing or skip it.
    # Scan carefully: "Whitespace is ignored."
    # So `(1 0x2)` is not valid? Or `A B` is `AB`?
    # I will `replace(" ", "").replace("\n", "")` just to be safe if that's what it means.
    # But usually markers don't contain spaces.
    # Let's trust `.strip()` for now. The file snippet showed one long line starting `EXGPFSKT...`.
    return decompressed_length(data)

def decompressed_length_v2(s):
    length = 0
    i = 0
    while i < len(s):
        if s[i] == '(':
            end_marker = s.find(')', i)
            if end_marker == -1:
                length += len(s) - i
                break
            
            marker = s[i+1:end_marker]
            parts = marker.split('x')
            if len(parts) != 2:
                length += 1
                i += 1
                continue
                
            chars_to_take = int(parts[0])
            repeat_count = int(parts[1])
            
            # Recursive call on the content
            content_start = end_marker + 1
            content_end = content_start + chars_to_take
            content = s[content_start:content_end]
            
            sub_len = decompressed_length_v2(content)
            length += sub_len * repeat_count
            
            i = content_end
        else:
            length += 1
            i += 1
    return length

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read().strip()
    return decompressed_length_v2(data)

def run_example():
    examples = [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18)
    ]
    print("Testing Part 1 examples:")
    for s, expected in examples:
        got = decompressed_length(s)
        print(f"'{s}' -> {got} (expected {expected})")
        
    examples_v2 = [
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20), # X + 2 * (3*3)ABC + Y = 1 + 18 + 1 = 20
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445)
    ]
    print("\nTesting Part 2 examples:")
    for s, expected in examples_v2:
        got = decompressed_length_v2(s)
        print(f"'{s}' -> {got} (expected {expected})")

if __name__ == "__main__":
    print("Testing examples:")
    run_example()
    print("\nPart 1:", part1())
    print("Part 2:", part2())

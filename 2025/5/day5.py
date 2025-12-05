import os
import sys


def load_input():
    input_path = os.path.join(sys.path[0], 'input.txt')
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        print("Warning: input.txt not found. Using example for testing.")
        # Example data for testing
        example_data = [
            "3-5",
            "10-14",
            "16-20",
            "12-18",
            "",
            "1",
            "5",
            "8",
            "11",
            "17",
            "32"
        ]
        return example_data


def part1(data):
    # Parse ranges and IDs from data
    # Format assumption: ranges as 'low-high' lines until blank, then one ID per line
    ranges = []
    ids = []
    parsing_ranges = True
    for line in data:
        if not line:
            parsing_ranges = False
            continue
        if parsing_ranges:
            if '-' in line:
                low, high = map(int, line.split('-'))
                ranges.append((low, high))
        else:
            try:
                ids.append(int(line))
            except ValueError:
                pass  # Skip non-numeric lines

    fresh_count = sum(1 for iid in ids if any(
        low <= iid <= high for low, high in ranges))
    return fresh_count


def part2(data):
    # Parse only ranges (up to blank or end; ignore IDs after)
    ranges = []
    for line in data:
        if not line:
            break  # Stop at blank line
        if '-' in line:
            low, high = map(int, line.split('-'))
            ranges.append((low, high))

    if not ranges:
        return 0

    # Merge overlapping/adjacent intervals
    ranges.sort()  # Sort by start
    merged = []
    current_start, current_end = ranges[0]
    for start, end in ranges[1:]:
        if start <= current_end + 1:  # Overlap or adjacent
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    merged.append((current_start, current_end))

    # Total unique IDs covered
    total = sum(end - start + 1 for start, end in merged)
    return total


if __name__ == '__main__':
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
    # Example Part 2 test (ranges only)
    example_ranges = [
        "3-5",
        "10-14",
        "16-20",
        "12-18"
    ]
    print("Example Part 2:", part2(example_ranges))  # Should be 14

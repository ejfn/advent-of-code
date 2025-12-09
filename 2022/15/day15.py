import os
import re
import sys
from textwrap import dedent


def parse(data: str):
    sensors = []
    pattern = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    for line in data.strip().splitlines():
        sx, sy, bx, by = map(int, pattern.match(line).groups())
        dist = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, bx, by, dist))
    return sensors


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def covered_positions_on_row(sensors, target_row):
    intervals = []
    beacons_on_row = set()
    for sx, sy, bx, by, dist in sensors:
        if by == target_row:
            beacons_on_row.add(bx)
        dy = abs(sy - target_row)
        if dy > dist:
            continue
        reach = dist - dy
        intervals.append((sx - reach, sx + reach))
    merged = merge_intervals(intervals)
    total = sum(end - start + 1 for start, end in merged)
    for x in beacons_on_row:
        for start, end in merged:
            if start <= x <= end:
                total -= 1
                break
    return total


def find_tuning_frequency(sensors, limit):
    pos_lines = set()
    neg_lines = set()
    for sx, sy, _, _, dist in sensors:
        d = dist + 1
        pos_lines.add(sy - sx + d)
        pos_lines.add(sy - sx - d)
        neg_lines.add(sy + sx + d)
        neg_lines.add(sy + sx - d)

    for pos in pos_lines:
        for neg in neg_lines:
            if (neg - pos) % 2 != 0:
                continue
            x = (neg - pos) // 2
            y = (pos + neg) // 2
            if not (0 <= x <= limit and 0 <= y <= limit):
                continue
            if all(abs(sx - x) + abs(sy - y) > dist for sx, sy, _, _, dist in sensors):
                return x * 4_000_000 + y
    raise ValueError("Distress beacon not found")


def part1(data: str, target_row: int) -> int:
    sensors = parse(data)
    return covered_positions_on_row(sensors, target_row)


def part2(data: str, limit: int) -> int:
    sensors = parse(data)
    return find_tuning_frequency(sensors, limit)


def run_example() -> None:
    example = dedent(
        """\
        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        Sensor at x=9, y=16: closest beacon is at x=10, y=16
        Sensor at x=13, y=2: closest beacon is at x=15, y=3
        Sensor at x=12, y=14: closest beacon is at x=10, y=16
        Sensor at x=10, y=20: closest beacon is at x=10, y=16
        Sensor at x=14, y=17: closest beacon is at x=10, y=16
        Sensor at x=8, y=7: closest beacon is at x=2, y=10
        Sensor at x=2, y=0: closest beacon is at x=2, y=10
        Sensor at x=0, y=11: closest beacon is at x=2, y=10
        Sensor at x=20, y=14: closest beacon is at x=25, y=17
        Sensor at x=17, y=20: closest beacon is at x=21, y=22
        Sensor at x=16, y=7: closest beacon is at x=15, y=3
        Sensor at x=14, y=3: closest beacon is at x=15, y=3
        Sensor at x=20, y=1: closest beacon is at x=15, y=3
        """
    )
    assert part1(example, 10) == 26
    assert part2(example, 20) == 56000011
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input, target_row=2_000_000))
    print(part2(puzzle_input, limit=4_000_000))

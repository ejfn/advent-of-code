#!/usr/bin/env python3
"""
Advent of Code 2023 Day 5: If You Give A Seed A Fertilizer
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Sequence, Tuple


Mapping = list[tuple[int, int, int]]


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip().splitlines()


def parse(lines: Iterable[str]) -> tuple[list[int], list[Mapping]]:
    iterator = iter(lines)
    seeds_line = next(iterator)
    seeds = [int(x) for x in seeds_line.split(":")[1].split()]

    mappings: list[Mapping] = []
    current: Mapping = []
    for line in iterator:
        line = line.strip()
        if not line:
            if current:
                mappings.append(current)
                current = []
            continue
        if line.endswith("map:"):
            if current:
                mappings.append(current)
                current = []
            continue
        dest, src, length = map(int, line.split())
        current.append((dest, src, length))
    if current:
        mappings.append(current)
    return seeds, mappings


def apply_maps(value: int, mappings: Sequence[Mapping]) -> int:
    for mapping in mappings:
        for dest, src, length in mapping:
            if src <= value < src + length:
                value = dest + (value - src)
                break
    return value


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else list(lines)
    seeds, mappings = parse(data)
    return min(apply_maps(seed, mappings) for seed in seeds)


def apply_range_map(ranges: list[tuple[int, int]], mapping: Mapping) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    for start, length in ranges:
        segments = [(start, length)]
        mapped: list[tuple[int, int]] = []
        for dest, src, span in mapping:
            next_segments: list[tuple[int, int]] = []
            src_end = src + span
            for seg_start, seg_len in segments:
                seg_end = seg_start + seg_len
                overlap_start = max(seg_start, src)
                overlap_end = min(seg_end, src_end)
                if overlap_start < overlap_end:
                    if seg_start < overlap_start:
                        next_segments.append((seg_start, overlap_start - seg_start))
                    mapped_start = dest + (overlap_start - src)
                    mapped.append((mapped_start, overlap_end - overlap_start))
                    if overlap_end < seg_end:
                        next_segments.append((overlap_end, seg_end - overlap_end))
                else:
                    next_segments.append((seg_start, seg_len))
            segments = next_segments
        result.extend(mapped)
        result.extend(segments)
    return result


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else list(lines)
    seeds, mappings = parse(data)
    ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for mapping in mappings:
        ranges = apply_range_map(ranges, mapping)
    return min(start for start, _ in ranges)


def run_example() -> None:
    example = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".splitlines()
    assert part1(example) == 35
    assert part2(example) == 46
    print("✓ Example checks passed (Part 1: 35, Part 2: 46)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

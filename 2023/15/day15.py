#!/usr/bin/env python3
"""
Advent of Code 2023 Day 15: Lens Library
"""

from __future__ import annotations

import os
import sys
from typing import Iterable, List, Tuple


def read_input() -> str:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def holiday_hash(s: str) -> int:
    value = 0
    for ch in s:
        value += ord(ch)
        value *= 17
        value %= 256
    return value


def part1(lines: Iterable[str] | None = None) -> int:
    text = read_input() if lines is None else "".join(lines).strip()
    return sum(holiday_hash(step) for step in text.split(",") if step)


def part2(lines: Iterable[str] | None = None) -> int:
    text = read_input() if lines is None else "".join(lines).strip()
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in text.split(","):
        if not step:
            continue
        if "=" in step:
            label, focal_str = step.split("=")
            focal = int(focal_str)
            box_idx = holiday_hash(label)
            box = boxes[box_idx]
            for idx, (existing_label, _) in enumerate(box):
                if existing_label == label:
                    box[idx] = (label, focal)
                    break
            else:
                box.append((label, focal))
        elif step.endswith("-"):
            label = step[:-1]
            box_idx = holiday_hash(label)
            box = boxes[box_idx]
            boxes[box_idx] = [entry for entry in box if entry[0] != label]

    total = 0
    for box_idx, box in enumerate(boxes, start=1):
        for slot_idx, (_, focal) in enumerate(box, start=1):
            total += box_idx * slot_idx * focal
    return total


def run_example() -> None:
    example = "HASH"
    assert holiday_hash(example) == 52

    text = "HASH"
    assert part1([text]) == 52

    bigger = "rn=1,cm-,qp=3"
    assert part1([bigger]) == sum(holiday_hash(step) for step in bigger.split(","))

    full_example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    assert part1([full_example]) == 1320
    assert part2([full_example]) == 145
    print("✓ Example checks passed (Part 1: 1320, Part 2: 145)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

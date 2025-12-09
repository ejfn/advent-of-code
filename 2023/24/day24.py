#!/usr/bin/env python3
"""
Advent of Code 2023 Day 24: Never Tell Me The Odds
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction
from typing import Iterable, List, Tuple

import sympy as sp


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse(lines: list[str]) -> list[tuple[int, int, int, int, int, int]]:
    hailstones = []
    for line in lines:
        pos_part, vel_part = line.split("@")
        px, py, pz = map(int, pos_part.replace(" ", "").split(","))
        vx, vy, vz = map(int, vel_part.replace(" ", "").split(","))
        hailstones.append((px, py, pz, vx, vy, vz))
    return hailstones


def intersection_xy(h1, h2):
    x1, y1, _, vx1, vy1, _ = h1
    x2, y2, _, vx2, vy2, _ = h2

    det = vx1 * (-vy2) - vy1 * (-vx2)
    if det == 0:
        return None

    dx = x2 - x1
    dy = y2 - y1

    det_t1 = dx * (-vy2) - dy * (-vx2)
    det_t2 = vx1 * dy - vy1 * dx

    t1 = Fraction(det_t1, det)
    t2 = Fraction(det_t2, det)

    if t1 < 0 or t2 < 0:
        return None

    intersect_x = Fraction(x1) + Fraction(vx1) * t1
    intersect_y = Fraction(y1) + Fraction(vy1) * t1
    return intersect_x, intersect_y


def part1(lines: Iterable[str] | None = None, test_min=None, test_max=None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    hailstones = parse(data)
    if test_min is None or test_max is None:
        max_val = max(abs(h[0]) for h in hailstones)
        if max_val < 1000:
            test_min, test_max = 7, 27
        else:
            test_min, test_max = 200000000000000, 400000000000000

    total = 0
    n = len(hailstones)
    for i in range(n):
        for j in range(i + 1, n):
            result = intersection_xy(hailstones[i], hailstones[j])
            if result is None:
                continue
            x, y = result
            if test_min <= x <= test_max and test_min <= y <= test_max:
                total += 1
    return total


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    hailstones = parse(data)

    rx, ry, rz, vx, vy, vz, t0, t1, t2 = sp.symbols("rx ry rz vx vy vz t0 t1 t2", integer=True)
    variables = (rx, ry, rz, vx, vy, vz, t0, t1, t2)
    eqs = []
    ts = [t0, t1, t2]

    for idx, hailstone in enumerate(hailstones[:3]):
        px, py, pz, hvx, hvy, hvz = hailstone
        ti = ts[idx]
        eqs.append(sp.Eq(rx + vx * ti, px + hvx * ti))
        eqs.append(sp.Eq(ry + vy * ti, py + hvy * ti))
        eqs.append(sp.Eq(rz + vz * ti, pz + hvz * ti))

    solution = sp.solve(eqs, variables, dict=True)[0]
    rx_val = int(solution[rx])
    ry_val = int(solution[ry])
    rz_val = int(solution[rz])
    return rx_val + ry_val + rz_val


def run_example() -> None:
    example = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""".splitlines()
    assert part1(example, 7, 27) == 2
    print("✓ Example check passed (Part 1)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

#!/usr/bin/env python3
"""
Advent of Code 2023 Day 20: Pulse Propagation
"""

from __future__ import annotations

import math
import os
import sys
from collections import deque
from typing import Dict, Iterable, List, Tuple


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


class Module:
    def __init__(self, name: str, mtype: str, outputs: list[str]):
        self.name = name
        self.type = mtype
        self.outputs = outputs


def parse_modules(lines: list[str]) -> tuple[dict[str, Module], dict[str, list[str]]]:
    modules: dict[str, Module] = {}
    for line in lines:
        left, right = line.split(" -> ")
        outputs = [part.strip() for part in right.split(",")]
        if left == "broadcaster":
            name = "broadcaster"
            mtype = "broadcaster"
        else:
            mtype = left[0]
            name = left[1:]
        modules[name] = Module(name, mtype, outputs)

    # build incoming map for conjunction modules
    incoming: dict[str, list[str]] = {}
    for module in modules.values():
        for dest in module.outputs:
            incoming.setdefault(dest, []).append(module.name)

    return modules, incoming


def simulate(
    modules: dict[str, Module],
    incoming: dict[str, list[str]],
    presses: int | None,
    watch_target: str | None = None,
) -> tuple[int, int, dict[str, int]]:
    flip_state = {name: False for name, module in modules.items() if module.type == "%"}
    conj_state = {
        name: {src: 0 for src in incoming.get(name, [])}
        for name, module in modules.items()
        if module.type == "&"
    }

    low_count = 0
    high_count = 0
    watch_hits: dict[str, int] = {}
    press = 0

    while presses is None or press < presses:
        press += 1
        queue = deque([("button", "broadcaster", 0)])

        while queue:
            src, dst, pulse = queue.popleft()
            if pulse == 0:
                low_count += 1
            else:
                high_count += 1

            if watch_target and dst == watch_target and pulse == 1 and src not in watch_hits:
                watch_hits[src] = press

            if dst not in modules:
                continue

            module = modules[dst]
            if module.type == "broadcaster":
                out_pulse = pulse
                for out in module.outputs:
                    queue.append((dst, out, out_pulse))
            elif module.type == "%":
                if pulse == 1:
                    continue
                flip_state[dst] = not flip_state[dst]
                out_pulse = 1 if flip_state[dst] else 0
                for out in module.outputs:
                    queue.append((dst, out, out_pulse))
            elif module.type == "&":
                if dst not in conj_state:
                    conj_state[dst] = {src_name: 0 for src_name in incoming.get(dst, [])}
                conj_state[dst][src] = pulse
                out_pulse = 0 if all(value == 1 for value in conj_state[dst].values()) else 1
                for out in module.outputs:
                    queue.append((dst, out, out_pulse))

        if presses is None:
            # We're running until watch target satisfied
            target_inputs = incoming.get(watch_target, [])
            if len(watch_hits) == len(target_inputs) and target_inputs:
                break

    return low_count, high_count, watch_hits


def part1(lines: Iterable[str] | None = None) -> int:
    lines = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    modules, incoming = parse_modules(lines)
    low, high, _ = simulate(modules, incoming, presses=1000)
    return low * high


def lcm(values: list[int]) -> int:
    result = 1
    for value in values:
        result = result * value // math.gcd(result, value)
    return result


def part2(lines: Iterable[str] | None = None) -> int:
    lines = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    modules, incoming = parse_modules(lines)

    target_module = None
    for module in modules.values():
        if "rx" in module.outputs:
            target_module = module.name
            break
    if not target_module:
        raise ValueError("No module feeds rx")

    _, _, watch_hits = simulate(modules, incoming, presses=None, watch_target=target_module)
    if not watch_hits:
        raise ValueError("No hits recorded for target")
    return lcm(list(watch_hits.values()))


def run_example() -> None:
    example1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".splitlines()
    assert part1(example1) == 32000000

    example2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""".splitlines()
    assert part1(example2) == 11687500
    print("✓ Example checks passed (Part 1)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

import os
import sys
from typing import List, Tuple

Instruction = Tuple[str, int]


def parse(data: str) -> List[Instruction]:
    program: List[Instruction] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        op, arg = line.split()
        program.append((op, int(arg)))
    return program


def run(program: List[Instruction]) -> Tuple[bool, int]:
    acc = 0
    ip = 0
    visited = set()
    while ip < len(program):
        if ip in visited:
            return False, acc
        visited.add(ip)
        op, arg = program[ip]
        if op == 'acc':
            acc += arg
            ip += 1
        elif op == 'jmp':
            ip += arg
        else:  # nop
            ip += 1
    return True, acc


def part1(data: str) -> int:
    program = parse(data)
    terminated, acc = run(program)
    assert not terminated
    return acc


def part2(data: str) -> int:
    program = parse(data)
    for i, (op, arg) in enumerate(program):
        if op not in {'nop', 'jmp'}:
            continue
        modified = program.copy()
        modified[i] = ('jmp' if op == 'nop' else 'nop', arg)
        terminated, acc = run(modified)
        if terminated:
            return acc
    raise RuntimeError('No fix found')


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    print("Example Part 1:", part1(example))  # Expected 5
    print("Example Part 2:", part2(example))  # Expected 8


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

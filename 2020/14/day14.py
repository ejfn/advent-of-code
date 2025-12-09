import os
import re
import sys
from typing import Dict, List

MASK_RE = re.compile(r'^mask = ([X01]{36})$')
MEM_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')


def parse(data: str) -> List[str]:
    return [line.strip() for line in data.splitlines() if line.strip()]


def part1(data: str) -> int:
    lines = parse(data)
    mask_or = 0
    mask_and = (1 << 36) - 1
    memory: Dict[int, int] = {}
    for line in lines:
        if line.startswith('mask = '):
            mask = line.split(' = ')[1]
            mask_or = int(mask.replace('X', '0'), 2)
            mask_and = int(mask.replace('X', '1'), 2)
        else:
            match = MEM_RE.match(line)
            assert match
            addr = int(match.group(1))
            value = int(match.group(2))
            value = (value | mask_or) & mask_and
            memory[addr] = value
    return sum(memory.values())


def generate_addresses(address: int, mask: str) -> List[int]:
    addr = list(f'{address:036b}')
    floating_positions: List[int] = []
    for i, ch in enumerate(mask):
        if ch == '0':
            continue
        if ch == '1':
            addr[i] = '1'
        elif ch == 'X':
            addr[i] = 'X'
            floating_positions.append(i)
    addresses: List[int] = []
    combinations = 1 << len(floating_positions)
    for combo in range(combinations):
        bits = f'{combo:0{len(floating_positions)}b}'
        addr_copy = addr[:]
        for bit, pos in zip(bits, floating_positions):
            addr_copy[pos] = bit
        addresses.append(int(''.join(addr_copy).replace('X', '0'), 2))
    return addresses


def part2(data: str) -> int:
    lines = parse(data)
    memory: Dict[int, int] = {}
    mask = 'X' * 36
    for line in lines:
        if line.startswith('mask = '):
            mask = line.split(' = ')[1]
        else:
            match = MEM_RE.match(line)
            assert match
            base_addr = int(match.group(1))
            value = int(match.group(2))
            for addr in generate_addresses(base_addr, mask):
                memory[addr] = value
    return sum(memory.values())


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    print("Example Part 1:", part1(example))  # Expected 165
    example2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    print("Example Part 2:", part2(example2))  # Expected 208


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

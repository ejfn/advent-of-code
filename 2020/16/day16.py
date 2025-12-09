import os
import sys
from typing import Dict, List, Tuple

Range = Tuple[int, int]
Rules = Dict[str, List[Range]]


def parse(data: str) -> Tuple[Rules, List[int], List[List[int]]]:
    sections = data.strip().split('\n\n')
    rules: Rules = {}
    for line in sections[0].splitlines():
        name, rest = line.split(': ')
        parts = rest.split(' or ')
        ranges = []
        for part in parts:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
        rules[name] = ranges
    your_ticket = [int(x) for x in sections[1].splitlines()[1].split(',')]
    nearby = [[int(x) for x in line.split(',')] for line in sections[2].splitlines()[1:]]
    return rules, your_ticket, nearby


def value_valid(value: int, rules: Rules) -> bool:
    for ranges in rules.values():
        for start, end in ranges:
            if start <= value <= end:
                return True
    return False


def part1(data: str) -> int:
    rules, _, nearby = parse(data)
    total = 0
    for ticket in nearby:
        for value in ticket:
            if not value_valid(value, rules):
                total += value
    return total


def field_valid_for_column(values: List[int], ranges: List[Range]) -> bool:
    for value in values:
        if not any(start <= value <= end for start, end in ranges):
            return False
    return True


def part2(data: str) -> int:
    rules, your_ticket, nearby = parse(data)
    valid_tickets = [ticket for ticket in nearby if all(value_valid(v, rules) for v in ticket)]
    valid_tickets.append(your_ticket)
    num_fields = len(your_ticket)
    column_values = [[ticket[i] for ticket in valid_tickets] for i in range(num_fields)]

    possibilities = {field: set(range(num_fields)) for field in rules}
    for field, ranges in rules.items():
        for idx, values in enumerate(column_values):
            if not field_valid_for_column(values, ranges):
                possibilities[field].discard(idx)

    assigned: Dict[str, int] = {}
    while possibilities:
        settled = [(field, next(iter(cols))) for field, cols in possibilities.items() if len(cols) == 1]
        if not settled:
            raise RuntimeError('Cannot resolve fields')
        for field, idx in settled:
            assigned[field] = idx
            del possibilities[field]
            for other in possibilities.values():
                other.discard(idx)

    result = 1
    for field, idx in assigned.items():
        if field.startswith('departure'):
            result *= your_ticket[idx]
    return result


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    print("Example Part 1:", part1(example))  # Expected 71


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

import os
import re
import sys
from functools import lru_cache
from typing import Dict, List, Tuple

LINE_RE = re.compile(r'^(?P<outer>[a-z ]+) bags contain (?P<inner>.+)\.$')
ITEM_RE = re.compile(r'(?P<count>\d+) (?P<color>[a-z ]+) bag')


def parse(data: str) -> Dict[str, List[Tuple[int, str]]]:
    rules: Dict[str, List[Tuple[int, str]]] = {}
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        match = LINE_RE.match(line)
        assert match
        outer = match.group('outer')
        inner_desc = match.group('inner')
        if inner_desc == 'no other bags':
            rules[outer] = []
        else:
            contents = []
            for item in inner_desc.split(', '):
                item_match = ITEM_RE.match(item)
                assert item_match
                count = int(item_match.group('count'))
                color = item_match.group('color')
                contents.append((count, color))
            rules[outer] = contents
    return rules


def build_reverse(rules: Dict[str, List[Tuple[int, str]]]) -> Dict[str, List[str]]:
    reverse: Dict[str, List[str]] = {}
    for outer, contents in rules.items():
        for _, color in contents:
            reverse.setdefault(color, []).append(outer)
    return reverse


def part1(data: str) -> int:
    rules = parse(data)
    reverse = build_reverse(rules)
    target = 'shiny gold'
    seen = set()
    stack = list(reverse.get(target, []))
    while stack:
        color = stack.pop()
        if color in seen:
            continue
        seen.add(color)
        stack.extend(reverse.get(color, []))
    return len(seen)


def part2(data: str) -> int:
    rules = parse(data)

    @lru_cache(maxsize=None)
    def count_inside(color: str) -> int:
        total = 0
        for qty, inner in rules.get(color, []):
            total += qty * (1 + count_inside(inner))
        return total

    return count_inside('shiny gold')


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """light red bags contain 1 bright white bag, 2 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    print("Example Part 1:", part1(example))  # Expected 4
    print("Example Part 2:", part2(example))  # Expected 32 for second sample


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

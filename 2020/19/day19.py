import os
import re
import sys
from typing import Dict, List, Tuple

Rules = Dict[str, str]
LIMIT = 5


def parse(data: str) -> Tuple[Rules, List[str]]:
    rules_raw, messages_raw = data.strip().split('\n\n')
    rules: Rules = {}
    for line in rules_raw.splitlines():
        idx, rule = line.split(': ')
        rules[idx] = rule.strip()
    messages = [line.strip() for line in messages_raw.splitlines() if line.strip()]
    return rules, messages


def build_regex(rule_id: str, rules: Rules, cache: Dict[str, str], part2: bool, base42: str, base31: str) -> str:
    if rule_id in cache:
        return cache[rule_id]

    if part2 and rule_id == '8':
        pattern = f'(?:{base42})+'
        cache[rule_id] = pattern
        return pattern
    if part2 and rule_id == '11':
        combos = [f'(?:{base42}){{{n}}}(?:{base31}){{{n}}}' for n in range(1, LIMIT + 1)]
        pattern = '(?:' + '|'.join(combos) + ')'
        cache[rule_id] = pattern
        return pattern

    rule = rules[rule_id]
    if '"' in rule:
        pattern = rule.replace('"', '')
        cache[rule_id] = pattern
        return pattern

    options = []
    for option in rule.split(' | '):
        parts = option.strip().split()
        subpatterns = [build_regex(part, rules, cache, part2, base42, base31) for part in parts]
        options.append(''.join(subpatterns))
    if len(options) == 1:
        pattern = options[0]
    else:
        pattern = '(?:' + '|'.join(options) + ')'
    cache[rule_id] = pattern
    return pattern


def compile_pattern(rules: Rules, part2: bool = False) -> re.Pattern[str]:
    cache: Dict[str, str] = {}
    base42 = build_regex('42', rules, cache, False, '', '')
    base31 = build_regex('31', rules, cache, False, '', '')
    if not part2:
        cache.clear()
    pattern = build_regex('0', rules, cache, part2, base42, base31)
    return re.compile('^' + pattern + '$')


def solve(data: str, part2: bool = False) -> int:
    rules, messages = parse(data)
    pattern = compile_pattern(rules, part2)
    return sum(bool(pattern.match(message)) for message in messages)


def part1(data: str) -> int:
    return solve(data, part2=False)


def part2(data: str) -> int:
    return solve(data, part2=True)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

aabbbbabbbb"""
    print("Example Part 1:", part1(example))


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

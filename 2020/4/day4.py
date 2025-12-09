import os
import re
import sys
from typing import Dict, List

REQUIRED_FIELDS = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
}

HCL_RE = re.compile(r'^#[0-9a-f]{6}$')
PID_RE = re.compile(r'^\d{9}$')
VALID_ECL = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def parse(data: str) -> List[Dict[str, str]]:
    passports: List[Dict[str, str]] = []
    for block in data.strip().split('\n\n'):
        fields: Dict[str, str] = {}
        for entry in block.split():
            key, value = entry.split(':', 1)
            fields[key] = value
        passports.append(fields)
    return passports


def has_required_fields(passport: Dict[str, str]) -> bool:
    return REQUIRED_FIELDS <= passport.keys()


def valid_height(value: str) -> bool:
    if value.endswith('cm'):
        try:
            num = int(value[:-2])
        except ValueError:
            return False
        return 150 <= num <= 193
    if value.endswith('in'):
        try:
            num = int(value[:-2])
        except ValueError:
            return False
        return 59 <= num <= 76
    return False


def is_valid(passport: Dict[str, str]) -> bool:
    if not has_required_fields(passport):
        return False
    try:
        byr = int(passport['byr'])
        iyr = int(passport['iyr'])
        eyr = int(passport['eyr'])
    except ValueError:
        return False
    if not (1920 <= byr <= 2002):
        return False
    if not (2010 <= iyr <= 2020):
        return False
    if not (2020 <= eyr <= 2030):
        return False
    if not valid_height(passport['hgt']):
        return False
    if not HCL_RE.match(passport['hcl']):
        return False
    if passport['ecl'] not in VALID_ECL:
        return False
    if not PID_RE.match(passport['pid']):
        return False
    return True


def part1(data: str) -> int:
    passports = parse(data)
    return sum(has_required_fields(p) for p in passports)


def part2(data: str) -> int:
    passports = parse(data)
    return sum(is_valid(p) for p in passports)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n\n\necl:gry\n"""
    print("Example Part 1:", part1(example1))


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

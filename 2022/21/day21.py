import operator
import os
import sys
from functools import lru_cache
from textwrap import dedent


OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parse(data: str):
    values = {}
    operations = {}
    for line in data.strip().splitlines():
        name, expr = line.split(": ")
        parts = expr.split()
        if len(parts) == 1:
            values[name] = int(parts[0])
        else:
            left, op, right = parts
            operations[name] = (left, op, right)
    return values, operations


def part1(data: str) -> int:
    values, operations = parse(data)

    @lru_cache(maxsize=None)
    def evaluate(name: str) -> int:
        if name in values:
            return values[name]
        left, op, right = operations[name]
        return OPS[op](evaluate(left), evaluate(right))

    return evaluate("root")


def part2(data: str) -> int:
    values, operations = parse(data)

    def contains_humn(name: str) -> bool:
        if name == "humn":
            return True
        if name in values:
            return False
        left, _, right = operations[name]
        return contains_humn(left) or contains_humn(right)

    @lru_cache(maxsize=None)
    def evaluate(name: str) -> int:
        if name in values:
            if name == "humn":
                raise ValueError("humn is unknown")
            return values[name]
        left, op, right = operations[name]
        return OPS[op](evaluate(left), evaluate(right))

    def safe_evaluate(name: str) -> int:
        if name == "humn":
            raise ValueError("humn is unknown")
        if name in values:
            return values[name]
        left, op, right = operations[name]
        try:
            return OPS[op](safe_evaluate(left), safe_evaluate(right))
        except ValueError:
            raise

    def solve(name: str, target: int) -> int:
        if name == "humn":
            return target
        left, op, right = operations[name]
        if contains_humn(left):
            other = safe_evaluate(right)
            if op == "+":
                new_target = target - other
            elif op == "-":
                new_target = target + other
            elif op == "*":
                new_target = target // other
            elif op == "/":
                new_target = target * other
            else:
                raise ValueError("Unknown op")
            return solve(left, new_target)
        else:
            other = safe_evaluate(left)
            if op == "+":
                new_target = target - other
            elif op == "-":
                new_target = other - target
            elif op == "*":
                new_target = target // other
            elif op == "/":
                new_target = other // target
            else:
                raise ValueError("Unknown op")
            return solve(right, new_target)

    left, _, right = operations["root"]
    if contains_humn(left):
        target = safe_evaluate(right)
        return solve(left, target)
    else:
        target = safe_evaluate(left)
        return solve(right, target)


def run_example() -> None:
    example = dedent(
        """\
        root: pppw + sjmn
        dbpl: 5
        cczh: sllz + lgvd
        zczc: 2
        ptdq: humn - dvpt
        dvpt: 3
        lfqf: 4
        humn: 5
        ljgn: 2
        sjmn: drzm * dbpl
        sllz: 4
        pppw: cczh / lfqf
        lgvd: ljgn * ptdq
        drzm: hmdt - zczc
        hmdt: 32
        """
    )
    assert part1(example) == 152
    assert part2(example) == 301
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

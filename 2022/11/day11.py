import math
import os
import sys
from collections import deque
from dataclasses import dataclass
from textwrap import dedent
from typing import Callable, List


@dataclass
class Monkey:
    items: List[int]
    operation: Callable[[int], int]
    divisor: int
    true_target: int
    false_target: int


def parse_operation(expr: str) -> Callable[[int], int]:
    _, _, rhs = expr.partition("=")
    rhs = rhs.strip()  # e.g. "old * 19"
    left, op, right = rhs.split()

    def get_operand(value: str, old: int) -> int:
        return old if value == "old" else int(value)

    if op == "+":
        return lambda old: get_operand(left, old) + get_operand(right, old)
    elif op == "*":
        return lambda old: get_operand(left, old) * get_operand(right, old)
    raise ValueError(f"Unknown operator {op}")


def parse(data: str) -> list[Monkey]:
    monkeys: list[Monkey] = []
    for block in data.strip().split("\n\n"):
        lines = [line.strip() for line in block.splitlines()]
        items = [int(value.strip()) for value in lines[1].split(":")[1].split(",")]
        operation = parse_operation(lines[2].split(":")[1].strip())
        divisor = int(lines[3].split()[-1])
        true_target = int(lines[4].split()[-1])
        false_target = int(lines[5].split()[-1])
        monkeys.append(Monkey(items, operation, divisor, true_target, false_target))
    return monkeys


def simulate(monkeys: list[Monkey], rounds: int, worry_relief: int | None) -> int:
    queues = [deque(monkey.items) for monkey in monkeys]
    inspections = [0] * len(monkeys)
    mod = math.prod(monkey.divisor for monkey in monkeys)

    for _ in range(rounds):
        for idx, monkey in enumerate(monkeys):
            while queues[idx]:
                inspections[idx] += 1
                worry = monkey.operation(queues[idx].popleft())
                if worry_relief:
                    worry //= worry_relief
                else:
                    worry %= mod
                target = monkey.true_target if worry % monkey.divisor == 0 else monkey.false_target
                queues[target].append(worry)

    top_two = sorted(inspections)[-2:]
    return top_two[0] * top_two[1]


def part1(data: str) -> int:
    monkeys = parse(data)
    return simulate(monkeys, rounds=20, worry_relief=3)


def part2(data: str) -> int:
    monkeys = parse(data)
    return simulate(monkeys, rounds=10_000, worry_relief=None)


def run_example() -> None:
    example = dedent(
        """\
        Monkey 0:
          Starting items: 79, 98
          Operation: new = old * 19
          Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3

        Monkey 1:
          Starting items: 54, 65, 75, 74
          Operation: new = old + 6
          Test: divisible by 19
            If true: throw to monkey 2
            If false: throw to monkey 0

        Monkey 2:
          Starting items: 79, 60, 97
          Operation: new = old * old
          Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3

        Monkey 3:
          Starting items: 74
          Operation: new = old + 3
          Test: divisible by 17
            If true: throw to monkey 0
            If false: throw to monkey 1
        """
    )
    assert part1(example) == 10605
    assert part2(example) == 2713310158
    print("✓ Example passed")


if __name__ == "__main__":
    run_example()
    with open(os.path.join(sys.path[0], "input.txt"), "r", encoding="utf-8") as f:
        puzzle_input = f.read().strip()
    print(part1(puzzle_input))
    print(part2(puzzle_input))

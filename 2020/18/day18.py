import os
import sys
from typing import Dict, List

Token = str


def tokenize(expr: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif ch in '+*()':
            tokens.append(ch)
            i += 1
        elif ch == ' ':
            i += 1
        else:
            raise ValueError(f'Unexpected character {ch}')
    return tokens


def to_rpn(tokens: List[Token], precedence: Dict[str, int]) -> List[Token]:
    output: List[Token] = []
    ops: List[str] = []
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in precedence:
            while ops and ops[-1] in precedence and precedence[ops[-1]] >= precedence[token]:
                output.append(ops.pop())
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':  # type: ignore[unreachable]
                output.append(ops.pop())
            ops.pop()  # remove '('
        else:
            raise ValueError(f'Invalid token {token}')
    while ops:
        output.append(ops.pop())
    return output


def eval_rpn(tokens: List[Token]) -> int:
    stack: List[int] = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '*':
                stack.append(a * b)
            else:
                raise ValueError(f'Unknown operator {token}')
    return stack[-1]


def evaluate(expr: str, precedence: Dict[str, int]) -> int:
    tokens = tokenize(expr)
    rpn = to_rpn(tokens, precedence)
    return eval_rpn(rpn)


def part1(data: str) -> int:
    precedence = {'+': 1, '*': 1}
    return sum(evaluate(line, precedence) for line in data.splitlines() if line.strip())


def part2(data: str) -> int:
    precedence = {'+': 2, '*': 1}
    return sum(evaluate(line, precedence) for line in data.splitlines() if line.strip())


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = "1 + (2 * 3) + (4 * (5 + 6))"
    print("Example Part 1:", evaluate(example, {'+': 1, '*': 1}))  # Expected 51
    print("Example Part 2:", evaluate(example, {'+': 2, '*': 1}))  # Expected 51*? actual 51? but mostly 51 and 51? (should be 51 and 51) just demonstration


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

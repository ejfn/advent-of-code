import os
import sys
from collections import deque
from typing import Deque, List, Tuple

Deck = Deque[int]


def parse(data: str) -> Tuple[Deck, Deck]:
    players = data.strip().split('\n\n')
    decks: List[Deck] = []
    for block in players:
        lines = block.splitlines()[1:]
        decks.append(deque(int(line) for line in lines if line.strip()))
    return decks[0], decks[1]


def score(deck: Deck) -> int:
    return sum((idx + 1) * card for idx, card in enumerate(reversed(deck)))


def play_simple(deck1: Deck, deck2: Deck) -> Deck:
    d1 = deque(deck1)
    d2 = deque(deck2)
    while d1 and d2:
        c1 = d1.popleft()
        c2 = d2.popleft()
        if c1 > c2:
            d1.extend([c1, c2])
        else:
            d2.extend([c2, c1])
    return d1 if d1 else d2


def recursive_combat(deck1: Deck, deck2: Deck) -> Tuple[int, Deck]:
    d1 = deque(deck1)
    d2 = deque(deck2)
    seen = set()
    while d1 and d2:
        state = (tuple(d1), tuple(d2))
        if state in seen:
            return 1, d1
        seen.add(state)
        c1 = d1.popleft()
        c2 = d2.popleft()
        if len(d1) >= c1 and len(d2) >= c2:
            winner, _ = recursive_combat(deque(list(d1)[:c1]), deque(list(d2)[:c2]))
        else:
            winner = 1 if c1 > c2 else 2
        if winner == 1:
            d1.extend([c1, c2])
        else:
            d2.extend([c2, c1])
    return (1, d1) if d1 else (2, d2)


def part1(data: str) -> int:
    deck1, deck2 = parse(data)
    winning_deck = play_simple(deck1, deck2)
    return score(winning_deck)


def part2(data: str) -> int:
    deck1, deck2 = parse(data)
    _, winning_deck = recursive_combat(deck1, deck2)
    return score(winning_deck)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    print("Example Part 1:", part1(example))  # Expected 306
    print("Example Part 2:", part2(example))  # Expected 291


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

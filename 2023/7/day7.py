#!/usr/bin/env python3
"""
Advent of Code 2023 Day 7: Camel Cards
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from typing import Iterable, List, Tuple


CARD_ORDER_PART1 = {c: i for i, c in enumerate("23456789TJQKA")}
CARD_ORDER_PART2 = {c: i for i, c in enumerate("J23456789TQKA")}


def read_input() -> list[str]:
    path = os.path.join(sys.path[0], "input.txt")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def evaluate_hand(hand: str, jokers_wild: bool) -> Tuple[int, List[int]]:
    if jokers_wild:
        return evaluate_with_jokers(hand)
    counts = Counter(hand)
    sorted_counts = sorted(counts.values(), reverse=True)
    hand_type = classify(sorted_counts)
    rank_values = [CARD_ORDER_PART1[c] for c in hand]
    return hand_type, rank_values


def classify(counts: list[int]) -> int:
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0


def evaluate_with_jokers(hand: str) -> Tuple[int, List[int]]:
    counts = Counter(c for c in hand if c != "J")
    joker_count = hand.count("J")
    if not counts:
        # five jokers
        return 6, [CARD_ORDER_PART2[c] for c in hand]

    sorted_counts = sorted(counts.values(), reverse=True)
    sorted_counts[0] += joker_count
    hand_type = classify(sorted_counts + [0] * (5 - len(sorted_counts)))
    rank_values = [CARD_ORDER_PART2[c] for c in hand]
    return hand_type, rank_values


def total_winnings(lines: Iterable[str], jokers_wild: bool) -> int:
    hands = []
    for line in lines:
        hand, bid_str = line.split()
        bid = int(bid_str)
        hand_type, ranks = evaluate_hand(hand, jokers_wild)
        hands.append(((hand_type, ranks), bid))

    hands.sort(key=lambda item: (item[0][0], item[0][1]))
    total = 0
    for idx, (_, bid) in enumerate(hands, start=1):
        total += bid * idx
    return total


def part1(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    return total_winnings(data, jokers_wild=False)


def part2(lines: Iterable[str] | None = None) -> int:
    data = read_input() if lines is None else [line.strip() for line in lines if line.strip()]
    return total_winnings(data, jokers_wild=True)


def run_example() -> None:
    example = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".splitlines()
    assert part1(example) == 6440
    assert part2(example) == 5905
    print("✓ Example checks passed (Part 1: 6440, Part 2: 5905)")


if __name__ == "__main__":
    if os.getenv("RUN_EXAMPLE", "0") == "1":
        run_example()
    print(part1())
    print(part2())

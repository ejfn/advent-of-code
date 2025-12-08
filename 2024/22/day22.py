import os
import sys
from collections import defaultdict, deque


MOD = 1 << 24
ROUNDS = 2000


def parse_input(filename):
    """Return list of initial secret numbers."""
    with open(filename) as f:
        return [int(line.strip()) for line in f if line.strip()]


def evolve(secret):
    """Apply the three mixing operations to advance the secret once."""
    secret = ((secret * 64) ^ secret) % MOD
    secret = ((secret // 32) ^ secret) % MOD
    secret = ((secret * 2048) ^ secret) % MOD
    return secret


def advance(secret, rounds=ROUNDS):
    """Advance a secret number multiple rounds."""
    for _ in range(rounds):
        secret = evolve(secret)
    return secret


def sum_final_secrets(starts, rounds=ROUNDS):
    """Part 1: sum secrets after `rounds` evolutions each."""
    return sum(advance(start, rounds) for start in starts)


def best_banana_total(starts, rounds=ROUNDS):
    """
    Part 2: Find the best 4-change sequence and return total bananas.
    Track first occurrence per buyer using a per-start seen set.
    """
    totals = defaultdict(int)
    window = deque(maxlen=4)

    for start in starts:
        seen = set()
        secret = start
        prev_price = secret % 10
        window.clear()

        for _ in range(rounds):
            secret = evolve(secret)
            price = secret % 10
            delta = price - prev_price
            prev_price = price
            window.append(delta)

            if len(window) == 4:
                key = tuple(window)
                if key not in seen:
                    totals[key] += price
                    seen.add(key)

    return max(totals.values()) if totals else 0


def part1():
    input_file = os.path.join(sys.path[0], "input.txt")
    starts = parse_input(input_file)
    return sum_final_secrets(starts)


def part2():
    input_file = os.path.join(sys.path[0], "input.txt")
    starts = parse_input(input_file)
    return best_banana_total(starts)


def run_example():
    starts = [1, 10, 100, 2024]
    print("Example part 1:", sum_final_secrets(starts))
    print("Example part 2:", best_banana_total(starts))


if __name__ == "__main__":
    print("=== Example ===")
    run_example()

    input_file = os.path.join(sys.path[0], "input.txt")
    if os.path.exists(input_file):
        print("\n=== Part 1 ===")
        print(part1())

        print("\n=== Part 2 ===")
        print(part2())
    else:
        print(
            "\nNo input.txt found in this directory. Add your puzzle input to run part 1 and part 2."
        )

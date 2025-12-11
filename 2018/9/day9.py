import sys
import os
import re
from collections import deque, defaultdict

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read().strip()
    match = re.search(r'(\d+) players; last marble is worth (\d+) points', content)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

def solve_game(num_players, last_marble):
    circle = deque([0])
    scores = defaultdict(int)
    
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % num_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
            
    return max(scores.values()) if scores else 0

def part1():
    num_players, last_marble = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_game(num_players, last_marble)
    print(f'Part 1: {result}')
    return result

def part2():
    num_players, last_marble = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_game(num_players, last_marble * 100)
    print(f'Part 2: {result}')
    return result

def run_example():
    print("Running Example...")
    # 9 players; last marble is worth 25 points: high score is 32
    assert solve_game(9, 25) == 32
    # 10 players; last marble is worth 1618 points: high score is 8317
    assert solve_game(10, 1618) == 8317
    # 13 players; last marble is worth 7999 points: high score is 146373
    assert solve_game(13, 7999) == 146373
    # 17 players; last marble is worth 1104 points: high score is 2764
    assert solve_game(17, 1104) == 2764
    # 21 players; last marble is worth 6111 points: high score is 54718
    assert solve_game(21, 6111) == 54718
    # 30 players; last marble is worth 5807 points: high score is 37305
    assert solve_game(30, 5807) == 37305
    print("Examples Passed")

if __name__ == '__main__':
    run_example()
    part1()
    part2()

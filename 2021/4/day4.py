import os
import sys
import numpy as np

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = list(filter(lambda s: len(s) > 0, [line.strip() for line in f]))

draw_numbers = np.fromstring(lines[0], dtype=int, sep=',')
boards = np.array([np.fromstring(j, dtype=int, sep=' ')
                   for j in filter(lambda i: i != '', lines[1:])]
                  ).reshape([-1, 5, 5])


def is_complete(board: np.array):
    chk = board == -1
    if np.any(np.all(chk, axis=0)) or np.any(np.all(chk, axis=1)):
        return True
    return False


def part1():
    for n in draw_numbers:
        for board in boards:
            board[board == n] = -1
            if is_complete(board):
                return board[board != -1].sum() * n


def part2():
    tmp = [*boards]
    for n in draw_numbers:
        for board in tmp:
            board[board == n] = -1
            if is_complete(board):
                win = board
                win_n = n
        tmp = list(filter(lambda b: not is_complete(b), tmp))
    return win[win != -1].sum() * win_n


print(part1())  # 49686
print(part2())  # 26878

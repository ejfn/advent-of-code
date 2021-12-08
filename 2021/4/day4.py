import os
import sys
import itertools

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = list(filter(lambda s: len(s) > 0, [line.strip() for line in f]))

draw_numbers = [int(i) for i in lines[0].split(',')]
boards = [[[(int(k), False) for k in j.split()] for j in lines[i:i+5]]
          for i in range(1, len(lines)-1, 5)]


def is_complete(board):
    for i in range(5):
        if all([board[i][j][1] for j in range(5)]) or all([board[j][i][1] for j in range(5)]):
            return True
    return False


def sum_board(board):
    return sum([i[0] if not i[1] else 0 for i in itertools.chain(*board)])


def draw(board, n):
    for i in range(5):
        for j in range(5):
            if board[i][j][0] == n:
                board[i][j] = (n, True)


def part1():
    for n in draw_numbers:
        for board in boards:
            draw(board, n)
            if is_complete(board):
                return sum_board(board) * n


def part2():
    tmp = [*boards]
    for n in draw_numbers:
        for board in tmp:
            draw(board, n)
            if is_complete(board):
                win = board
                win_n = n
        tmp = list(filter(lambda b: not is_complete(b), tmp))
    return sum_board(win) * win_n


print(part1())
print(part2())

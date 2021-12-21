import functools
import itertools as it

start = (7, 8)


def play_determ(player, next_player, times=0):
    pos, score = player
    dice = (9 * times + 3) % 100 + 3
    pos = (pos + dice - 1) % 10 + 1
    score += pos
    if score >= 1000:
        return (times + 1) * 3 * next_player[1]
    return play_determ(next_player, (pos, score), times + 1)


def part1():
    print(play_determ(*zip(start, [0, 0])))


@functools.cache
def play_dirac(player, next_player):
    if next_player[1] >= 21:
        return 0, 1  # previous won!
    pos, score = player
    win1, win2 = 0, 0
    for dice in it.product([1, 2, 3], repeat=3):
        pos1 = (pos + sum(dice) - 1) % 10 + 1
        score1 = score + pos1
        w2, w1 = play_dirac(next_player, (pos1, score1))
        win1 += w1
        win2 += w2
    return win1, win2


def part2():
    w1, w2 = play_dirac(*zip(start, [0, 0]))
    print(max([w1, w2]))


part1()  # 556206
part2()  # 630797200227453

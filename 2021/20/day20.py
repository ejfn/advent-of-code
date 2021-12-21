from functools import reduce
import os
import sys
import numpy as np
import itertools as it

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    lines = f.readlines()
    algorithm = [1 if c == '#' else 0 for c in lines[0].strip()]
    input = np.array([[1 if c == '#' else 0 for c in line.strip()]
                     for line in lines[2:]])


def resolve(i: int, j: int, arr: np.array):
    bit_arr_reverse = [
        arr[i+1, j+1], arr[i+1, j], arr[i+1, j-1],
        arr[i, j+1], arr[i, j], arr[i, j-1],
        arr[i-1, j+1], arr[i-1, j], arr[i-1, j-1]
    ]
    val = reduce(lambda x, y: x+y,
                 [x * 2 ** i for i, x in enumerate(bit_arr_reverse)])
    return algorithm[val]


def apply(input: np.array):
    output = np.zeros(input.shape, dtype=int)
    m, n = output.shape
    for x, y in it.product(range(1, m-1), range(1, n-1)):
        output[x, y] = resolve(x, y, input)
    return output


def apply_twice(input: np.array):
    x = np.pad(input, ((4, 4), (4, 4)), 'constant')  # padding
    x = apply(apply(x))  # apply twice let infinites go zero
    return x[2:-2, 2:-2]  # unpadding non-zero marigins


def part1():
    print(np.sum(apply_twice(input)))


def part2():
    x = input
    for _ in range(25):
        x = apply_twice(x)
    print(np.sum(x))


part1()  # 5275
part2()  # 16482

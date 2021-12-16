from functools import reduce
import os
import sys
import math

with open(os.path.join(sys.path[0], 'input.txt'), 'rb') as f:
    line = bin(int(f.readline().strip(), 16))[2:]


def decode(pos: int) -> tuple[int, int, int]:
    ver = int(line[pos:pos + 3], 2)
    type = int(line[pos + 3: pos + 6], 2)
    val = 0
    if type == 4:
        # literal
        pos += 6
        bin = ''
        while line[pos] == '1':
            pos += 5
            bin += line[pos-4:pos]
        pos += 5
        bin += line[pos-4:pos]
        val = int(bin, 2)
    else:
        # operator
        sub = []
        pos += 6
        if line[pos] == '0':
            pos += 16
            n = pos + int(line[pos-15:pos], 2)
            while pos < n:
                v, x, pos = decode(pos)
                ver += v
                sub.append(x)
        else:
            pos += 12
            n = int(line[pos-11:pos], 2)
            for _ in range(n):
                v, x, pos = decode(pos)
                ver += v
                sub.append(x)
        match type:
            case 0:
                val = sum(sub)
            case 1:
                val = reduce(lambda x, y: x * y, sub)
            case 2:
                val = min(sub)
            case 3:
                val = max(sub)
            case 5:
                val = 1 if sub[0] > sub[1] else 0
            case 6:
                val = 1 if sub[0] < sub[1] else 0
            case 7:
                val = 1 if sub[0] == sub[1] else 0
    return (ver, val, math.ceil(pos))


ver, val, _ = decode(0)

print(ver)  # 974
print(val)  # 180616437720

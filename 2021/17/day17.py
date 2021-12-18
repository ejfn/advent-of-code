import math

x1, x2 = 287, 309
y1, y2 = -76, -48


def part1():
    return y1 * (y1 + 1) // 2


def part2():
    x_hits, y_hits = [], []
    x_min = math.floor(math.sqrt(x1 * 2))
    # fine all velocity x and nth step hit target
    for x in range(x_min, x2 + 1):
        t, n = 0, 1
        while t <= x2 and n <= x:
            t = n * x - n * (n-1) // 2
            if x1 <= t <= x2:
                x_hits.append((x, n))
            n += 1
    # fine all velocity y and nth step hit target
    for y in range(y1, -y1):
        t, n = 0, 1 if y < 0 else 2 * y
        while t >= y1:
            t = n * y - n * (n - 1) // 2
            if y1 <= t <= y2:
                y_hits.append((y, n))
            n += 1
    result = []
    for (x, xn) in x_hits:
        for (y, yn) in y_hits:
            # equal, or greater than when x == 0 at target
            if xn == yn or yn > xn == x:
                result.append((x, y))
    result = list(set(result))
    return len(result)


print(part1())  # 2850
print(part2())  # 1117

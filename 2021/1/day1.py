import os
import sys

with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    numbers = [int(i) for i in f.readlines()]

p1 = len(
    list(filter(lambda i: numbers[i] < numbers[i+1], range(0, len(numbers) - 1))))
p2 = len(list(filter(lambda i: sum(
    numbers[i:i+3]) < sum(numbers[i+1:i+4]), range(0, len(numbers) - 3))))

print(p1)
print(p2)

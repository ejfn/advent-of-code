import os
import sys
import math
from binarytree import Node
from functools import reduce


def createNode(x, depth=-1):
    if isinstance(x, list):
        l = createNode(x[0], depth - 1)
        r = createNode(x[1], depth - 1)
        return Node(depth, l, r)
    else:
        return Node(x)


lines = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        lines.append(eval(line.strip()))


def add(x: Node, y: Node):
    for i in x.inorder + y.inorder:
        if i.value < 0:
            i.value -= 1  # increase level
    root = Node(-1, x, y)
    while reduceNode(root):
        continue
    return root


def reduceNode(root: Node):
    l = root.inorder
    for i in range(len(l)):
        n = l[i]
        if n.value <= -5:
            # explode
            for j in range(i - 2, -1, -1):
                if l[j].value >= 0:
                    l[j].value += n.left.value
                    break
            for j in range(i + 2, len(l), 1):
                if l[j].value >= 0:
                    l[j].value += n.right.value
                    break
            n.value = 0
            n.left = n.right = None
            return True
    l = root.inorder
    for i in range(len(l)):
        n = l[i]
        if n.value >= 10:
            # split
            n.left = Node(math.floor(n.value / 2))
            n.right = Node(math.ceil(n.value / 2))
            if l[i-1].right == n:
                n.value = l[i-1].value - 1
            elif l[i+1].left == n:
                n.value = l[i+1].value - 1
            return True
    return False


def magnitude(node: Node):
    if node.value < 0:
        l = magnitude(node.left)
        r = magnitude(node.right)
        return 3 * l + 2 * r
    else:
        return node.value


def part1():
    root = reduce(lambda x, y: add(x, y), [createNode(i) for i in lines])
    print(root)
    return magnitude(root)


def part2():
    l = len(lines)
    max_v = 0
    for i in range(0, l - 1):
        for j in range(i + 1, l):
            m = magnitude(add(createNode(lines[i]), createNode(lines[j])))
            n = magnitude(add(createNode(lines[j]), createNode(lines[i])))
            max_v = max(max_v, m, n)
    return max_v


print(part1())  # 4435
print(part2())  # 4802

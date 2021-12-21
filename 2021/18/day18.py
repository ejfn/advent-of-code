import os
import sys
import math
from binarytree import Node
from functools import reduce
import itertools


def createNode(x, depth=-1):
    if isinstance(x, list):
        # depth as value
        return Node(depth, createNode(x[0], depth - 1), createNode(x[1], depth - 1))
    else:
        # value as value for leaves
        return Node(x)


lines = []
with open(os.path.join(sys.path[0], 'input.txt'), 'r') as f:
    for line in f:
        lines.append(eval(line.strip()))


def add(x: Node, y: Node):
    for i in x.inorder + y.inorder:
        if i.value < 0:
            i.value -= 1  # decrease level
    root = Node(-1, x, y)
    while reduceNode(root.inorder):
        continue
    return root


def reduceNode(nodes: list[Node]):
    for i in range(len(nodes)):
        n = nodes[i]
        if n.value <= -5:
            # search left
            for j in range(i - 2, -1, -1):
                if nodes[j].value >= 0:
                    nodes[j].value += n.left.value
                    break
            # search right
            for j in range(i + 2, len(nodes), 1):
                if nodes[j].value >= 0:
                    nodes[j].value += n.right.value
                    break
            n.value = 0
            n.left = n.right = None
            nodes = nodes[:i - 2] + [n] + nodes[i + 2:]
            return True
    for i in range(len(nodes)):
        n = nodes[i]
        if n.value >= 10:
            # split
            n.left = Node(math.floor(n.value / 2))
            n.right = Node(math.ceil(n.value / 2))
            # depth = parent's depth - 1
            if nodes[i-1].right == n:
                n.value = nodes[i-1].value - 1
            elif nodes[i+1].left == n:
                n.value = nodes[i+1].value - 1
            nodes = nodes[:i - 1] + [n.left, n, n.right] + nodes[i + 1:]
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
    print(magnitude(root))


def part2():
    l = len(lines)
    max_v = 0
    for i, j in itertools.combinations(range(l), 2):
        m = magnitude(add(createNode(lines[i]), createNode(lines[j])))
        n = magnitude(add(createNode(lines[j]), createNode(lines[i])))
        max_v = max(max_v, m, n)
    print(max_v)


part1()  # 4435
part2()  # 4802

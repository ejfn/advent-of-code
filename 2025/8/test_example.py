import os
import sys
import heapq
from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def get_circuit_sizes(self):
        circuits = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuits[root] += 1
        return list(circuits.values())

def distance_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2

input_path = os.path.join(sys.path[0], 'example.txt')
with open(input_path) as f:
    lines = f.read().strip().split('\n')

# Parse junction box positions
boxes = []
for line in lines:
    x, y, z = map(int, line.split(','))
    boxes.append((x, y, z))

n = len(boxes)

# Calculate all pairwise distances and store in a min heap
distances = []
for i in range(n):
    for j in range(i + 1, n):
        dist_sq = distance_squared(boxes[i], boxes[j])
        heapq.heappush(distances, (dist_sq, i, j))

# Union-Find to track circuits
uf = UnionFind(n)

# Connect the 10 shortest pairs (for example)
connections = 0
while connections < 10 and distances:
    dist_sq, i, j = heapq.heappop(distances)
    if uf.union(i, j):
        connections += 1

# Get circuit sizes
circuit_sizes = uf.get_circuit_sizes()
circuit_sizes.sort(reverse=True)

print(f"Circuit sizes: {circuit_sizes}")
print(f"Three largest: {circuit_sizes[0]}, {circuit_sizes[1]}, {circuit_sizes[2]}")

# Multiply the three largest
result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
print(f"Result: {result}")
print(f"Expected: 40")

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

# Keep connecting until we have only one circuit
last_i, last_j = -1, -1
connections = 0
while len(uf.get_circuit_sizes()) > 1 and distances:
    dist_sq, i, j = heapq.heappop(distances)
    if uf.union(i, j):
        last_i, last_j = i, j
        connections += 1
        if connections >= 18:  # Print last few connections
            print(f"Connection {connections}: {boxes[i]} (idx {i}) to {boxes[j]} (idx {j})")

print(f"\nTotal connections: {connections}")
print(f"Last connection: {boxes[last_i]} to {boxes[last_j]}")
print(f"X coordinates: {boxes[last_i][0]} * {boxes[last_j][0]} = {boxes[last_i][0] * boxes[last_j][0]}")
print(f"Expected: 216 * 117 = 25272")

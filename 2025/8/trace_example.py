import os
import sys
import math

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
        from collections import defaultdict
        circuits = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuits[root] += 1
        return sorted(circuits.values(), reverse=True)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

input_path = os.path.join(sys.path[0], 'example.txt')
with open(input_path) as f:
    lines = f.read().strip().split('\n')

# Parse junction box positions
boxes = []
box_to_idx = {}
for idx, line in enumerate(lines):
    x, y, z = map(int, line.split(','))
    boxes.append((x, y, z))
    box_to_idx[(x, y, z)] = idx

n = len(boxes)

# Calculate all pairwise distances
distances = []
for i in range(n):
    for j in range(i + 1, n):
        dist = distance(boxes[i], boxes[j])
        distances.append((dist, i, j, boxes[i], boxes[j]))

distances.sort()

# Union-Find
uf = UnionFind(n)

# Make connections following the problem's description
connections_made = 0

# 1st: 162,817,812 to 425,690,689
idx1 = box_to_idx[(162,817,812)]
idx2 = box_to_idx[(425,690,689)]
print(f"1. Connect {boxes[idx1]} (idx {idx1}) to {boxes[idx2]} (idx {idx2})")
if uf.union(idx1, idx2):
    connections_made += 1
print(f"   Sizes: {uf.get_circuit_sizes()}")

# 2nd: 162,817,812 to 431,825,988
idx1 = box_to_idx[(162,817,812)]
idx2 = box_to_idx[(431,825,988)]
print(f"2. Connect {boxes[idx1]} (idx {idx1}) to {boxes[idx2]} (idx {idx2})")
if uf.union(idx1, idx2):
    connections_made += 1
print(f"   Sizes: {uf.get_circuit_sizes()}")

# 3rd: 906,360,560 to 805,96,715
idx1 = box_to_idx[(906,360,560)]
idx2 = box_to_idx[(805,96,715)]
print(f"3. Connect {boxes[idx1]} (idx {idx1}) to {boxes[idx2]} (idx {idx2})")
if uf.union(idx1, idx2):
    connections_made += 1
print(f"   Sizes: {uf.get_circuit_sizes()}")

# 4th would be: 431,825,988 to 425,690,689 but they're already connected
idx1 = box_to_idx[(431,825,988)]
idx2 = box_to_idx[(425,690,689)]
print(f"4. Try connect {boxes[idx1]} (idx {idx1}) to {boxes[idx2]} (idx {idx2})")
if uf.union(idx1, idx2):
    connections_made += 1
    print("   Connected!")
else:
    print("   Already in same circuit, skip")
print(f"   Sizes: {uf.get_circuit_sizes()}")

# Continue with remaining connections
print(f"\nContinuing with shortest distances until we have 10 connections...")
print(f"Connections made so far: {connections_made}\n")

for dist, i, j, b1, b2 in distances:
    if connections_made >= 10:
        break
    if uf.union(i, j):
        connections_made += 1
        print(f"{connections_made}. Connect {b1} (idx {i}) to {b2} (idx {j}), distance {dist:.2f}")

print(f"\nFinal circuit sizes: {uf.get_circuit_sizes()}")
print(f"Product of three largest: {uf.get_circuit_sizes()[0] * uf.get_circuit_sizes()[1] * uf.get_circuit_sizes()[2]}")

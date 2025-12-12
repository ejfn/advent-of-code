
import sys

# Increase recursion limit for connected components search if needed
sys.setrecursionlimit(20000)

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    points = []
    for line in lines:
        line = line.strip()
        if not line: continue
        coords = tuple(map(int, line.split(',')))
        points.append(coords)
        
    return points

def manhattan_dist(p1, p2):
    return sum(abs(a - b) for a, b in zip(p1, p2))

def solve_part1(filename):
    points = parse_input(filename)
    n = len(points)
    
    # We can use Union-Find or BFS/DFS to find connected components
    # N is around ~1500, so O(N^2) is ~2.25M checks, which is fine
    
    parent = list(range(n))
    
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False
        
    # Check all pairs
    # Optimize: spatial hashing? N^2 is likely fast enough.
    
    for i in range(n):
        for j in range(i + 1, n):
            if manhattan_dist(points[i], points[j]) <= 3:
                union(i, j)
                
    # Count unique roots
    constellations = set()
    for i in range(n):
        constellations.add(find(i))
        
    return len(constellations)

def run_example():
    ex1 = """ 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""
    
    # ... more examples ...
    
    import tempfile
    import os
    
    def test(raw_input, expected):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write(raw_input)
            tmp_name = tmp.name
        try:
            res = solve_part1(tmp_name)
            print(f"Example result: {res} (Expected {expected})")
            assert res == expected
        finally:
            os.remove(tmp_name)

    test(ex1, 2)
    
    ex4 = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""
    
    test(ex4, 8)
    print("Examples passed!")

if __name__ == '__main__':
    run_example()
    
    import os
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")

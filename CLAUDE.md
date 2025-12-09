# CLAUDE.md

Guidance for Claude Code when working with Advent of Code solutions.

## Repository Structure

```
YYYY/
└── N/
    ├── dayN.py    # Solution with part1() and part2() functions
    └── input.txt  # Puzzle input
```

**Code Pattern:**
- Load input: `os.path.join(sys.path[0], 'input.txt')`
- Implement: `part1()` and `part2()` functions
- Output: Print results from `if __name__ == "__main__"`
- Libraries: Any Python package (`os`, `sys`, `itertools`, `numpy`, `networkx`, `sympy`, etc.)
- No shared utilities between days

**Running:** `python YYYY/N/dayN.py`

## Problem-Solving Workflow

1. **Read carefully** - Don't assume input format. Summarize the core mechanics in your own words before coding.
2. **Example first** - Create `run_example()` with hardcoded sample input. Print parsed structures and validate against expected output before running on full input.
3. **Test incrementally** - Verify each part works. On errors, re-check parsing first.
4. **Performance target** - No puzzle should take >30 seconds. If slow, rethink the algorithm.

## Parsing Tips

- Read format carefully: char-by-char vs whitespace-separated, handle empty lines.
- Debug parsing first: print parsed data on example, verify structure (grid dims, value ranges).
- For grids: `grid = [[int(c) for c in line] for line in lines if line.strip()]`

## Performance Tips (When Slow)

**Quick fixes:**
- `set()` for O(1) lookups
- `collections.deque` for BFS queues
- `@functools.cache` for recursive memoization

**Algorithm issues:**
- If >10s, brute force won't work. Look for: known algorithms, mathematical properties, structural patterns.
- Avoid O(n² × cost) - preprocess to make inner checks O(1) via prefix sums, sparse tables, coordinate compression.
- Sort candidates by potential value descending; early-terminate when remaining can't beat best.

## Lessons from Past Days

- **2024 Day 24 Part 2**: When finding defects in structured systems (circuits, graphs), analyze expected patterns rather than testing all combinations. Define structural invariants, find violations directly.
- **2025 Day 9 Part 2**: When checking O(n²) candidate pairs, don't let each validation be O(area). Preprocess data structures for O(1) checks. Use coordinate compression. Sort by potential and early-terminate.

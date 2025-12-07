# CLAUDE.md

Guidance for Claude Code when working with Advent of Code solutions in this repository.

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
- Output: Print results directly from `if __name__ == "__main__"`
- Libraries: Any Python package can be installed and used as needed
  - Common: `os`, `sys`, `itertools`, `numpy`, `scipy`, `networkx`, `sympy`
  - Install with: `pip install <package>`
- No shared utilities between days

**Running:** `cd YYYY/N && python dayN.py`

## Problem-Solving Workflow

1. **Read problem carefully** - Don't assume input format
2. **Create example test file** - Validate parsing before running on full input
3. **Test incrementally** - Verify each part works before moving forward
4. **Watch error messages** - Unexpected values often indicate parsing errors, not logic issues

## Parsing and Input Handling

**Key Principles:**
- Character-level vs token-level: Know when to analyze char-by-char vs split on whitespace
- Whitespace matters: Count spaces, look for patterns in spacing/indentation
- Boundary detection: Empty lines, blank columns, or repeated patterns often separate sections
- Directionality: Consider all possible traversal directions and transformations

**Debugging:**
- Print parsed structures on small examples first
- Verify data types and values match expected format
- Re-read problem statement multiple times if results don't match

## Performance Guidelines

**Combinatorial Problems:**
- Avoid `itertools.combinations` if n > 15 (exponential time)
- Prefer: Greedy stack algorithms (monotonic stack) or DP
- Example: C(20,12) ≈ 10^6+

**Common Optimizations:**
- Arrays: `numpy`
- Queues: `collections.deque`
- Lookups: `set()` for O(1)
- Recursion: Add memoization if slow
- Loops: Test Part 2 with examples first to catch infinite loops

**Profiling:**
- Use `cProfile` for bottlenecks
- Add print statements to track progress
- Watch for dead loops in graph traversals
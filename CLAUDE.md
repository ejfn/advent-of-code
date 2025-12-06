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
3. **Test Part 1 thoroughly** - Part 2 often changes interpretation completely
4. **Watch error messages** - "Number too large" usually means parsing error, not math issue
5. **Update CLAUDE.md** - Add lessons learned after each day

## Parsing and Input Handling

**Key Principles:**
- Character-level vs token-level: Know when to analyze char-by-char vs split on whitespace
- Space patterns encode structure: Single space vs multiple spaces often matters
- Vertical column analysis: Use completely blank columns to detect boundaries
- Part 2 can reverse direction: Left-to-right ↔ right-to-left, rows ↔ columns

**Debugging:**
- Print parsed structures on small examples first
- Verify numbers and operations before computing results
- Re-read problem statement multiple times if parsing seems wrong

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
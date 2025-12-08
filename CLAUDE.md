# CLAUDE.md

Guidance for Claude Code when working with Advent of Code solutions in this repository.

**Efficiency Note**: Focus on Workflow + Parsing for most days; skip others unless needed. Always prioritize example testing to cut iterations.

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

**Running:** `python YYYY/N/dayN.py`

## Problem-Solving Workflow

1. **Read problem carefully** - Don't assume input format; summarize core mechanics (e.g., "What counts as visible?").
2. **Parse and test example first** - Hardcode/create sample input in a `run_example()` function. Print parsed structure (e.g., grid shape/values) and validate against expected outputs before full input.
3. **Test incrementally** - Verify each part works; re-check parsing on errors.
4. **Watch error messages** - Unexpected values often indicate parsing issues.

## Parsing Tips

**Read input format carefully:**
- Parse char-by-char or by whitespace; handle empty lines/spaces.

**Debug parsing first:**
- Print parsed data on example; verify expectations.
- For numeric grids: `grid = [[int(c) for c in line] for line in lines if line.strip()]`; print first 2-3 rows.

## Performance Tips (Apply if Slow/Hanging)

**Common optimizations:**
- `set()` for lookups; `collections.deque` for queues; `@cache` for recursion; `numpy` for arrays.

**If hangs:**
- Check infinite loops with prints.
- Avoid large combos (n>15); try greedy/DP/math.
- Profile: `python -m cProfile dayN.py`; time sections.

## Common Pitfalls (Lessons from Past Days)

- **Misreading Mechanics** (e.g., Day 8: antennas vs. tree visibility): Summarize post-read; test against examples.
- **Example Gaps**: Always `run_example()` with prints; verify grid dims (e.g., Day 8: 99x99 heights 0-9).
- **Over-Complexity**: Skip pair-wise/vector math; use edge scans (e.g., track max_height per direction) with bounds checks.
- **Parsing Oversights**: Convert to nums early; print to confirm.
- **Iteration Control**: Use todos for phases (e.g., "Parse example" → "One edge" → "Full Part 1"); re-read if stuck.
- **Brute Force vs. Structure**: When finding defects in structured systems (circuits, graphs, networks), analyze expected patterns rather than testing all combinations. Define structural invariants, find violations directly. If brute force >10s, look for domain knowledge (known algorithms, mathematical properties, structural rules).
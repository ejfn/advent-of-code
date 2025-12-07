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

**Running:** `python YYYY/N/dayN.py`

## Problem-Solving Workflow

1. **Read problem carefully** - Don't assume input format
2. **Create example test file** - Use the example input from the puzzle description
3. **Test with example first** - Validate parsing and logic on example before running on full input
4. **Test incrementally** - Verify each part works before moving forward
5. **Watch error messages** - Unexpected values often indicate parsing errors, not logic issues

## Parsing Tips

**Read the input format carefully:**
- Check if you need to parse character-by-character or split by whitespace
- Look for empty lines that separate sections
- Pay attention to spaces and indentation patterns

**Debug parsing first:**
- Print the parsed data structure on the example input
- Verify it matches what you expect before solving the problem
- If answers are wrong, re-check parsing before debugging logic

## Performance Tips

**Common optimizations:**
- Use `set()` for membership checks instead of lists
- Use `collections.deque` for queues instead of lists
- Add `@cache` decorator to recursive functions
- Use `numpy` for large array operations

**If your solution hangs:**
- First check: is it an infinite loop? Add print statements to see if it's making progress
- If it's trying too many combinations (like `itertools.combinations` with n > 15), you need a different algorithm
- Look for: greedy approaches, dynamic programming, or mathematical formulas

**Finding bottlenecks:**
- Run `python -m cProfile your_script.py` to see which functions are slow
- Add timing prints to measure specific sections
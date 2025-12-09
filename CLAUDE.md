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

- **Dependencies:** If you `pip install` a new package (directly or via `requirements.txt`), immediately add it to `requirements.txt` in the repo so the workflow stays reproducible.
- **Postmortems:** When a day's puzzle requires multiple iterations or hits a performance snag, add a concise “Lessons Learned” note to this file describing the issue and the eventual fix (algorithm change, data structure, etc.) after you resolve it.

## Daily Automation Instructions

Use this checklist for both the GitHub Action and local agents. Assume the environment variables `YEAR`, `DAY`, and `AOC_SESSION` are exported (the automation scripts set them for you).

**Exact filenames (do not change):**
- Puzzle: `${YEAR}/${DAY}/puzzle.md`
- Input: `${YEAR}/${DAY}/input.txt`
- Solution: `${YEAR}/${DAY}/day${DAY}.py` (no alternate names!)

**Steps:**
1. Read this CLAUDE.md for guidelines before coding.
2. Fetch the puzzle + input: `FORCE_DAY=$DAY FORCE_YEAR=$YEAR python aoc-automation/solve_daily.py`
3. Open `puzzle.md` and check whether either part is already solved:
   - If both parts show “Your puzzle answer was...”: stop immediately.
   - If only Part 1 is solved: jump to Step 7.
   - Otherwise continue.
4. Implement the solution in `day${DAY}.py`. Keep everything (part1/part2, run_example, main) in that file—no test_* helpers.
5. Test with a hard timeout: `timeout 30 python ${YEAR}/${DAY}/day${DAY}.py`
   - If it times out, rethink the approach; follow the Performance Tips below.
6. Submit answers via `python aoc-automation/submit_answer.py <part> <answer> $DAY $YEAR`.
7. Re-run Step 2 before tackling Part 2 (the site text often changes).
8. Implement `part2()`, re-test, re-submit, and capture the results as you did for Part 1.

**Local tip:** When running the automation manually, source `.env` (which holds `AOC_SESSION`) before Step 2 so the script can authenticate, e.g. `set -a; source .env; set +a`. Even on a local run, still finish Steps 6 and 8 (submit answers) once you have the results; skipping the commit is fine, but never skip submissions.

**Critical reminders:**
- Never skip the filename pattern—AoC automation expects `day${DAY}.py`.
- Always keep puzzle, input, and solution files together; automation assumes they live under the same day folder.
- If you install a new dependency, update `requirements.txt` when you introduce it.
- Before wrapping up a local run, check `git status` and make sure the entire day folder (plus `puzzle.md`/`input.txt`) is staged for the eventual commit.
- When solving multiple days in one request, handle them sequentially (finish coding/testing/submitting for a day before touching the next). Parallel progress across days makes submissions and tracking messy.
- When creating commits, explicitly thank and acknowledge the AI model that assisted in the session within the commit message so reviewers know which agent produced the work.

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

Add a short note here whenever a day's solution required multiple iterations or ran into a performance issue—summarize the problem and the eventual fix so future runs avoid the same trap.

- **2024 Day 24 Part 2**: When finding defects in structured systems (circuits, graphs), analyze expected patterns rather than testing all combinations. Define structural invariants, find violations directly.
- **2025 Day 9 Part 2**: When checking O(n²) candidate pairs, don't let each validation be O(area). Preprocess data structures for O(1) checks. Use coordinate compression. Sort by potential and early-terminate.

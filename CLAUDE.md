# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Setup
Install dependencies:
```
pip install numpy scipy binarytree
```
Use Python 3.10 or later (3.13 recommended).

### Running Solutions
Navigate to the year and day directory, then execute the solution:
```
cd 2021/1
python day1.py
```
This runs both parts and prints answers.

### Linting and Formatting
- Format with autopep8: `autopep8 --in-place dayN.py`
- Lint with pycodestyle: `pycodestyle dayN.py`

No build process or automated tests exist.

## Architecture

Solutions are organized by year (e.g., 2020, 2021) with subdirectories for each day (1-25). Each day directory contains:
- `dayN.py`: Self-contained Python script implementing solutions for both puzzle parts.
- `input.txt`: Puzzle input data.

Scripts load input using `os.path.join(sys.path[0], 'input.txt')` from the script's directory, compute answers in `part1()` and `part2()` functions, and print results directly. Common libraries include `os`, `sys`, `itertools`, and `numpy` for array operations.

The repository focuses on complete 2021 puzzles, partial 2020, and emerging 2025 solutions. Code follows a consistent pattern without shared utilities or modules across days.

## Performance Tips for AoC Puzzles

- Advent of Code often involves combinatorial problems; for selecting k elements from n (e.g., largest subsequence), avoid brute-force `itertools.combinations` if n > 15 as it leads to exponential time (C(n,k) ~ 10^6+ for n=20,k=12). Prefer O(n) greedy stack algorithms (monotonic stack to remove smallest digits while preserving order) or DP.
- Test Part Two with small example inputs first to catch long-running loops or dead loops (e.g., infinite recursion in graph traversals).
- Use efficient libraries: `numpy` for array operations, `collections.deque` for queues, and sets for O(1) lookups to prevent timeouts.
- If a solution hangs, profile with `cProfile` or add print statements to identify bottlenecks, then optimize (e.g., memoization for recursive functions).
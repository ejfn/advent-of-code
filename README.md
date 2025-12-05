# Advent of Code Solutions

Answers and solutions for [Advent of Code](https://adventofcode.com/).

## Repository Structure

Solutions are organized by year (e.g., `2020/`, `2021/`, `2025/`) with subdirectories for each day (1-25). Each day directory contains:
- `dayN.py`: Self-contained Python script implementing solutions for both puzzle parts.
- `input.txt`: Puzzle input data (personal; download from AoC site).

Current progress:
- 2020: Partial (Days 1-2).
- 2021: Complete (all 25 days).
- 2025: Days 1-5 implemented.

Code follows a consistent pattern without shared utilities across days. No build process or automated tests.

## Setup and Running

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   (Requires Python 3.10+; 3.13 recommended.)

2. Run a day's solution (from repo root):
   ```
   python3 202X/N/dayN.py
   ```
   This loads `input.txt` from the day's directory, computes answers for both parts, and prints them.

Example for 2025 Day 5:
```
python3 2025/5/day5.py
```

## Common Libraries

Scripts use standard libraries like `os`, `sys`, `itertools`, plus `numpy` for array operations.

## Performance Tips

- For combinatorial problems, avoid brute-force if n > 15; use greedy stacks or DP.
- Test Part 2 with examples first to catch loops/timeouts.
- Use `numpy` for arrays, `collections.deque` for queues, sets for O(1) lookups.

For issues or contributions, see [CLAUDE.md](CLAUDE.md) for internal guidance.
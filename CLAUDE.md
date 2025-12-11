# CLAUDE.md

Guidance for AI models when working with Advent of Code solutions.

## IMPORTANT: Use the Skill

**When working on Advent of Code puzzles, you MUST use the skill at `.claude/skills/aoc-daily-solver/SKILL.md`.**

Read the skill file first and follow its complete workflow. Do not attempt to solve puzzles without consulting the skill - it contains the automation scripts, problem-solving guidelines, parsing tips, performance optimization strategies, and lessons learned from past puzzles.

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
- **Postmortems:** When a day's puzzle requires multiple iterations or hits a performance snag, add a concise "Lessons Learned" note to `.claude/skills/aoc-daily-solver/SKILL.md` describing the issue and the eventual fix (algorithm change, data structure, etc.) after you resolve it.

## Automation Workflow

For the complete automation workflow, problem-solving guidelines, and lessons learned, see `.claude/skills/aoc-daily-solver/SKILL.md`.

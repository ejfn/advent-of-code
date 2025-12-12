#!/usr/bin/env python3
"""
Refresh all puzzle.md files for solved puzzles.

This script finds all solved puzzles (those with dayN.py files) and re-fetches
their puzzle descriptions to ensure puzzle.md contains both parts with their
confirmed answers.

Usage:
    # Load environment first
    set -a; source .env; set +a
    
    # Run the script
    python3 .claude/skills/aoc-daily-solver/scripts/refresh_all_puzzles.py
"""

import os
import sys
import time
import re
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from aoc_client import AoCClient


def find_solved_puzzles(repo_root: Path) -> list[tuple[int, int]]:
    """Find all year/day combinations that have a solution file."""
    puzzles = []
    
    for year_dir in sorted(repo_root.iterdir()):
        if not year_dir.is_dir():
            continue
        
        # Match year directories like 2017, 2018, etc.
        if not re.match(r'^20\d{2}$', year_dir.name):
            continue
        
        year = int(year_dir.name)
        
        for day_dir in sorted(year_dir.iterdir()):
            if not day_dir.is_dir():
                continue
            
            # Check if there's a dayN.py file
            try:
                day = int(day_dir.name)
            except ValueError:
                continue
            
            solution_file = day_dir / f"day{day}.py"
            if solution_file.exists():
                puzzles.append((year, day))
    
    return puzzles


def refresh_puzzle(session: str, year: int, day: int, work_dir: Path) -> bool:
    """Refresh the puzzle.md for a specific day."""
    puzzle_path = work_dir / "puzzle.md"
    
    try:
        client = AoCClient(session, year)
        puzzle_md = client.get_puzzle_markdown(day)
        
        # Write puzzle
        puzzle_path.write_text(puzzle_md)
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    
    # Get session
    session = os.getenv('AOC_SESSION')
    if not session:
        print("❌ AOC_SESSION environment variable not set")
        print("   Run: set -a; source .env; set +a")
        sys.exit(1)
    
    # Find all solved puzzles
    print("🔍 Finding solved puzzles...")
    puzzles = find_solved_puzzles(repo_root)
    print(f"   Found {len(puzzles)} solved puzzles\n")
    
    if not puzzles:
        print("No solved puzzles found.")
        return
    
    # Track progress
    success = 0
    failed = 0
    
    print("📥 Refreshing puzzle.md files...\n")
    
    for i, (year, day) in enumerate(puzzles, 1):
        work_dir = repo_root / str(year) / str(day)
        print(f"[{i}/{len(puzzles)}] {year} Day {day}...", end=" ", flush=True)
        
        if refresh_puzzle(session, year, day, work_dir):
            print("✓")
            success += 1
        else:
            failed += 1
        
        # Rate limiting - be nice to the AoC server
        if i < len(puzzles):
            time.sleep(0.5)  # 500ms between requests
    
    print(f"\n✅ Done! Refreshed {success} puzzles.")
    if failed:
        print(f"❌ Failed: {failed} puzzles")


if __name__ == "__main__":
    main()


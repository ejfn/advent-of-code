#!/usr/bin/env python3
"""
Daily AoC Solver Orchestrator
Fetches puzzle, prepares files, and coordinates with the solver.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from aoc_client import AoCClient


def main():
    # Get configuration
    year = int(os.getenv('FORCE_YEAR', os.getenv('YEAR', '2025')))
    day_str = os.getenv('FORCE_DAY', str(datetime.now().day))

    # Handle "today" input
    if day_str.lower() == 'today':
        day = datetime.now().day
    else:
        day = int(day_str)

    dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'

    # Get session cookie
    session = os.getenv('AOC_SESSION')
    if not session:
        print("❌ Error: AOC_SESSION environment variable not set")
        sys.exit(1)

    print(f"🎄 Advent of Code {year} Day {day}")
    print(f"{'🧪 DRY RUN MODE' if dry_run else '🚀 LIVE MODE'}")
    print()

    # Initialize client
    client = AoCClient(session, year)

    # Create working directory
    work_dir = Path(f"{year}/{day}")
    work_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Working directory: {work_dir}")

    # Fetch puzzle
    print(f"📥 Fetching puzzle...")
    try:
        puzzle_md = client.get_puzzle_markdown(day)
        puzzle_file = work_dir / "puzzle.md"
        puzzle_file.write_text(puzzle_md)
        print(f"✓ Puzzle saved to {puzzle_file}")
    except Exception as e:
        print(f"❌ Failed to fetch puzzle: {e}")
        sys.exit(1)

    # Fetch input
    print(f"📥 Fetching input...")
    try:
        input_data = client.get_input(day)
        input_file = work_dir / "input.txt"
        input_file.write_text(input_data)
        print(f"✓ Input saved to {input_file} ({len(input_data)} bytes)")
    except Exception as e:
        print(f"❌ Failed to fetch input: {e}")
        sys.exit(1)

    # Read CLAUDE.md for guidelines
    claude_md = Path("CLAUDE.md")
    guidelines = ""
    if claude_md.exists():
        guidelines = claude_md.read_text()
        print(f"✓ Loaded guidelines from CLAUDE.md")
    else:
        print(f"⚠️  CLAUDE.md not found, AI will solve without project guidelines")

    # No longer need to create prompt.txt - AI reads files directly

    # Export environment variables for workflow
    print()
    print("📋 Environment variables:")
    print(f"YEAR={year}")
    print(f"DAY={day}")
    print(f"WORK_DIR={work_dir}")

    # Save to GitHub Actions output if running in CI
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"year={year}\n")
            f.write(f"day={day}\n")
            f.write(f"work_dir={work_dir}\n")

    print()
    print("✅ Setup complete!")
    print()
    print("Next steps:")
    print("1. AI Agent will generate the solution")
    print("2. Test the solution by running it")
    print("3. Submit the answer to AoC")

    # Check if already solved
    try:
        answer1 = client.get_answer_from_page(day, 1)
        answer2 = client.get_answer_from_page(day, 2)

        if answer1:
            print()
            print(f"ℹ️  Note: Part 1 already solved (answer: {answer1})")
        if answer2:
            print(f"ℹ️  Note: Part 2 already solved (answer: {answer2})")

        if answer1 and answer2:
            print()
            print("⚠️  Both parts already solved! Use this for testing only.")
    except:
        pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Submit answer to Advent of Code
"""

import os
import sys
import time
from aoc_client import AoCClient


def main():
    if len(sys.argv) < 3:
        print("Usage: python submit_answer.py <part> <answer> [day] [year]")
        sys.exit(1)

    part = int(sys.argv[1])
    answer = sys.argv[2]
    day = int(sys.argv[3]) if len(sys.argv) > 3 else int(os.getenv('DAY', '1'))
    year = int(sys.argv[4]) if len(sys.argv) > 4 else int(os.getenv('YEAR', '2025'))

    dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'

    # Get session cookie
    session = os.getenv('AOC_SESSION')
    if not session:
        print("❌ Error: AOC_SESSION environment variable not set")
        sys.exit(1)

    print(f"📤 Submitting answer for {year} Day {day} Part {part}")
    print(f"   Answer: {answer}")

    if dry_run:
        print("🧪 DRY RUN - Not actually submitting")
        print("✓ Would have submitted successfully")
        sys.exit(0)

    # Submit answer
    client = AoCClient(session, year)

    try:
        result = client.submit_answer(day, part, answer)

        # Extract the article content for Claude to read
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(result['message'], 'html.parser')
        article = soup.find('article')

        print("\n" + "="*70)
        print("RESPONSE FROM ADVENT OF CODE:")
        print("="*70)
        if article:
            print(article.get_text().strip())
        else:
            print(result['message'][:500])
        print("="*70 + "\n")

    except Exception as e:
        print(f"❌ Error submitting answer: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

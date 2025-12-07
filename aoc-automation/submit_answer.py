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

        # Set output for workflow
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"status=correct\n")
                f.write(f"answer={answer}\n")
        sys.exit(0)

    # Submit answer
    client = AoCClient(session, year)

    try:
        result = client.submit_answer(day, part, answer)

        status = result['status']
        feedback = result.get('feedback')
        wait_time = result.get('wait_time', 0)

        if status == 'correct':
            print("✅ CORRECT! The answer is right!")
        elif status == 'already_solved':
            print("ℹ️  Already solved this part")
        elif status == 'wrong':
            print(f"❌ WRONG ANSWER")
            if feedback == 'too_high':
                print("   Hint: Your answer is too high")
            elif feedback == 'too_low':
                print("   Hint: Your answer is too low")
        elif status == 'rate_limit':
            print(f"⏳ Rate limited - wait {wait_time}s before trying again")
            if wait_time > 0:
                print(f"   Waiting {wait_time} seconds...")
                time.sleep(wait_time)
        else:
            print(f"⚠️  Unknown status: {status}")

        # Set output for workflow
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"status={status}\n")
                f.write(f"answer={answer}\n")
                if feedback:
                    f.write(f"feedback={feedback}\n")

        # Exit code
        if status in ['correct', 'already_solved']:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error submitting answer: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

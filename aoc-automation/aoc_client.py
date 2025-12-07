#!/usr/bin/env python3
"""
Advent of Code HTTP Client
Handles fetching puzzles, inputs, and submitting answers.
"""

import requests
from bs4 import BeautifulSoup
import re


class AoCClient:
    def __init__(self, session_cookie: str, year: int):
        """
        Initialize AoC client with session cookie.

        Args:
            session_cookie: Session cookie value from adventofcode.com
            year: Year to solve (e.g., 2025)
        """
        self.session = requests.Session()
        self.session.cookies.set('session', session_cookie, domain='.adventofcode.com')
        self.year = year
        self.base_url = f"https://adventofcode.com/{year}"

    def get_puzzle_html(self, day: int) -> str:
        """Fetch raw puzzle HTML"""
        url = f"{self.base_url}/day/{day}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def get_puzzle_markdown(self, day: int) -> str:
        """
        Fetch puzzle description as markdown.
        Converts HTML to clean text for Claude.
        """
        html = self.get_puzzle_html(day)
        soup = BeautifulSoup(html, 'html.parser')

        # Find all puzzle articles (Part 1 and Part 2 if unlocked)
        articles = soup.find_all('article', class_='day-desc')

        if not articles:
            raise ValueError(f"No puzzle found for day {day}")

        markdown_parts = []

        for idx, article in enumerate(articles):
            part_num = idx + 1
            markdown_parts.append(f"## Part {part_num}\n")
            markdown_parts.append(self._html_to_markdown(article))
            markdown_parts.append("\n")

        return "\n".join(markdown_parts)

    def _html_to_markdown(self, element) -> str:
        """Convert HTML element to markdown (simple version)"""
        # Get text content
        text = element.get_text()

        # Basic cleanup
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)

    def get_input(self, day: int) -> str:
        """Download personalized puzzle input"""
        url = f"{self.base_url}/day/{day}/input"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def submit_answer(self, day: int, part: int, answer: str) -> dict:
        """
        Submit answer to AoC.

        Returns:
            dict with keys:
                - status: 'correct' | 'wrong' | 'rate_limit' | 'already_solved'
                - message: Full response text
                - feedback: 'too_high' | 'too_low' | None (for wrong answers)
                - wait_time: seconds to wait (for rate limits)
        """
        url = f"{self.base_url}/day/{day}/answer"
        data = {'level': str(part), 'answer': str(answer).strip()}

        # Add headers to mimic browser behavior
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': f'{self.base_url}/day/{day}',
            'Origin': 'https://adventofcode.com',
        }

        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()

        html = response.text
        html_lower = html.lower()

        # Parse response - check for correct answers first
        if "that's the right answer" in html_lower or "that's right" in html_lower:
            return {
                'status': 'correct',
                'message': html,
                'feedback': None,
                'wait_time': 0
            }

        elif "did you already complete it" in html_lower or "already complete" in html_lower:
            return {
                'status': 'already_solved',
                'message': html,
                'feedback': None,
                'wait_time': 0
            }

        elif "answer too recently" in html_lower or ("you have" in html_lower and "left to wait" in html_lower):
            # Extract wait time
            wait_time = self._parse_wait_time(html)
            return {
                'status': 'rate_limit',
                'message': html,
                'feedback': None,
                'wait_time': wait_time
            }

        elif "too high" in html_lower:
            return {
                'status': 'wrong',
                'message': html,
                'feedback': 'too_high',
                'wait_time': 0
            }

        elif "too low" in html_lower:
            return {
                'status': 'wrong',
                'message': html,
                'feedback': 'too_low',
                'wait_time': 0
            }

        elif "not the right answer" in html_lower or "that's not right" in html_lower:
            return {
                'status': 'wrong',
                'message': html,
                'feedback': None,
                'wait_time': 0
            }

        else:
            # Unknown response - log it for debugging
            print(f"⚠️  Unknown response from AoC:")
            print(f"First 500 chars: {html[:500]}")
            return {
                'status': 'unknown',
                'message': html,
                'feedback': None,
                'wait_time': 0
            }

    def _parse_wait_time(self, html: str) -> int:
        """Parse wait time from rate limit message"""
        # Look for patterns like "5m 23s" or "42s" or "1m 2s"
        match = re.search(r'(\d+)m\s*(\d+)s', html)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            return minutes * 60 + seconds

        match = re.search(r'(\d+)s', html)
        if match:
            return int(match.group(1))

        match = re.search(r'(\d+)m', html)
        if match:
            return int(match.group(1)) * 60

        # Default to 60 seconds if can't parse
        return 60

    def get_answer_from_page(self, day: int, part: int) -> str | None:
        """
        Get the answer if already solved (from the puzzle page).
        Returns None if not solved yet.
        """
        html = self.get_puzzle_html(day)

        # Look for "Your puzzle answer was X"
        pattern = r'Your puzzle answer was <code>([^<]+)</code>'
        matches = re.findall(pattern, html)

        if matches and len(matches) >= part:
            return matches[part - 1]

        return None


if __name__ == '__main__':
    # Quick test
    import os
    import sys

    session = os.getenv('AOC_SESSION')
    if not session:
        print("Set AOC_SESSION environment variable")
        sys.exit(1)

    client = AoCClient(session, 2025)

    # Test with Day 1
    print("Testing with Day 1...")

    try:
        puzzle = client.get_puzzle_markdown(1)
        print(f"✓ Fetched puzzle ({len(puzzle)} chars)")

        input_data = client.get_input(1)
        print(f"✓ Fetched input ({len(input_data)} chars)")

        # Check if already solved
        answer = client.get_answer_from_page(1, 1)
        if answer:
            print(f"✓ Part 1 already solved: {answer}")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

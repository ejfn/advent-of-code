import os
import sys
from collections import defaultdict
import re

def parse_input(filename):
    """Parse and sort the guard logs."""
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    # Sort chronologically
    lines.sort()

    # Parse events
    events = []
    for line in lines:
        # Extract timestamp and action
        match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)', line)
        if match:
            timestamp, action = match.groups()
            events.append((timestamp, action))

    return events

def build_sleep_schedule(events):
    """Build a dictionary of guard -> minute -> count of times asleep."""
    guard_sleep = defaultdict(lambda: defaultdict(int))

    current_guard = None
    sleep_start = None

    for timestamp, action in events:
        if 'begins shift' in action:
            # Extract guard ID
            match = re.search(r'#(\d+)', action)
            if match:
                current_guard = int(match.group(1))
                sleep_start = None
        elif 'falls asleep' in action:
            # Extract minute from timestamp
            minute = int(timestamp.split(':')[1])
            sleep_start = minute
        elif 'wakes up' in action:
            # Extract minute from timestamp
            minute = int(timestamp.split(':')[1])
            if current_guard is not None and sleep_start is not None:
                # Mark all minutes from sleep_start to minute-1 as asleep
                for m in range(sleep_start, minute):
                    guard_sleep[current_guard][m] += 1
                sleep_start = None

    return guard_sleep

def part1():
    events = parse_input(os.path.join(sys.path[0], 'input.txt'))
    guard_sleep = build_sleep_schedule(events)

    # Find guard with most total sleep minutes
    max_sleep = 0
    sleepiest_guard = None

    for guard_id, sleep_minutes in guard_sleep.items():
        total_sleep = sum(sleep_minutes.values())
        if total_sleep > max_sleep:
            max_sleep = total_sleep
            sleepiest_guard = guard_id

    # Find the minute that guard was asleep most often
    sleep_by_minute = guard_sleep[sleepiest_guard]
    best_minute = max(sleep_by_minute.keys(), key=lambda m: sleep_by_minute[m])

    return sleepiest_guard * best_minute

def part2():
    events = parse_input(os.path.join(sys.path[0], 'input.txt'))
    guard_sleep = build_sleep_schedule(events)

    # Find guard/minute pair with highest frequency
    max_frequency = 0
    best_guard = None
    best_minute = None

    for guard_id, sleep_minutes in guard_sleep.items():
        for minute, count in sleep_minutes.items():
            if count > max_frequency:
                max_frequency = count
                best_guard = guard_id
                best_minute = minute

    return best_guard * best_minute

def run_example():
    """Test with the example from the puzzle."""
    example = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

    lines = example.strip().split('\n')
    lines.sort()

    events = []
    for line in lines:
        match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)', line)
        if match:
            timestamp, action = match.groups()
            events.append((timestamp, action))

    guard_sleep = build_sleep_schedule(events)

    # Verify Guard #10 slept 50 minutes total
    guard_10_total = sum(guard_sleep[10].values())
    print(f"Guard #10 total sleep: {guard_10_total} (expected 50)")

    # Verify Guard #99 slept 30 minutes total
    guard_99_total = sum(guard_sleep[99].values())
    print(f"Guard #99 total sleep: {guard_99_total} (expected 30)")

    # Find sleepiest guard and their most common minute
    max_sleep = 0
    sleepiest_guard = None
    for guard_id, sleep_minutes in guard_sleep.items():
        total_sleep = sum(sleep_minutes.values())
        if total_sleep > max_sleep:
            max_sleep = total_sleep
            sleepiest_guard = guard_id

    sleep_by_minute = guard_sleep[sleepiest_guard]
    best_minute = max(sleep_by_minute.keys(), key=lambda m: sleep_by_minute[m])

    print(f"Part 1: Guard #{sleepiest_guard}, minute {best_minute}, answer = {sleepiest_guard * best_minute} (expected 240)")

if __name__ == "__main__":
    print("Running example test:")
    run_example()
    print("\nSolving puzzle:")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

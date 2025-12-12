import os
import sys
import re


def parse_input(text):
    """Parse Turing machine blueprint."""
    lines = text.strip().split('\n')
    
    # Parse initial state and steps
    start_state = re.search(r'Begin in state (\w+)', lines[0]).group(1)
    steps = int(re.search(r'after (\d+) steps', lines[1]).group(1))
    
    # Parse states
    states = {}
    current_state = None
    current_value = None
    
    for line in lines[3:]:
        line = line.strip()
        if not line:
            continue
        
        state_match = re.match(r'In state (\w+):', line)
        if state_match:
            current_state = state_match.group(1)
            states[current_state] = {}
            continue
        
        value_match = re.match(r'If the current value is (\d+):', line)
        if value_match:
            current_value = int(value_match.group(1))
            states[current_state][current_value] = {}
            continue
        
        write_match = re.match(r'- Write the value (\d+)', line)
        if write_match:
            states[current_state][current_value]['write'] = int(write_match.group(1))
            continue
        
        move_match = re.match(r'- Move one slot to the (left|right)', line)
        if move_match:
            states[current_state][current_value]['move'] = 1 if move_match.group(1) == 'right' else -1
            continue
        
        next_match = re.match(r'- Continue with state (\w+)', line)
        if next_match:
            states[current_state][current_value]['next'] = next_match.group(1)
            continue
    
    return start_state, steps, states


def part1(start_state, steps, states):
    """Run Turing machine and return checksum (count of 1s on tape)."""
    tape = set()  # Positions with value 1
    cursor = 0
    state = start_state
    
    for _ in range(steps):
        current_val = 1 if cursor in tape else 0
        rule = states[state][current_val]
        
        # Write
        if rule['write'] == 1:
            tape.add(cursor)
        elif cursor in tape:
            tape.remove(cursor)
        
        # Move
        cursor += rule['move']
        
        # Next state
        state = rule['next']
    
    return len(tape)


def run_example():
    example = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""
    start_state, steps, states = parse_input(example)
    assert part1(start_state, steps, states) == 3
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        start_state, steps, states = parse_input(f.read())
    
    print(f"Part 1: {part1(start_state, steps, states)}")
    print("Part 2: Day 25 only has one part - collect all stars to complete!")

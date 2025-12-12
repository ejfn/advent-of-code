import sys
import os
import re
from collections import defaultdict

def solve(part1_target=None):
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    bots = defaultdict(list)
    instructions = {} # bot_id -> (low_type, low_id, high_type, high_id)
    outputs = defaultdict(list)
    
    # queues
    ready_bots = []

    # Parse
    for line in lines:
        if line.startswith('value'):
            # value V goes to bot B
            match = re.search(r'value (\d+) goes to bot (\d+)', line)
            val = int(match.group(1))
            bot_id = int(match.group(2))
            bots[bot_id].append(val)
        elif line.startswith('bot'):
            # bot B gives low to T1 I1 and high to T2 I2
            match = re.search(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', line)
            bot_id = int(match.group(1))
            low_type = match.group(2)
            low_id = int(match.group(3))
            high_type = match.group(4)
            high_id = int(match.group(5))
            instructions[bot_id] = (low_type, low_id, high_type, high_id)

    # Initial check for ready bots
    for bot_id, chips in bots.items():
        if len(chips) == 2:
            ready_bots.append(bot_id)

    part1_ans = None

    while ready_bots:
        bot_id = ready_bots.pop(0)
        chips = bots[bot_id]
        # Should have exactly 2 chips
        if len(chips) != 2:
            continue
            
        low = min(chips)
        high = max(chips)
        
        # Check Part 1 condition
        if part1_target and low == part1_target[0] and high == part1_target[1]:
            part1_ans = bot_id

        # Clear chips? Or just processed?
        # "gives each one...". So bot is empty after.
        bots[bot_id] = []
        
        # Execute instruction
        if bot_id in instructions:
            l_type, l_id, h_type, h_id = instructions[bot_id]
            
            # Give low
            if l_type == 'bot':
                bots[l_id].append(low)
                if len(bots[l_id]) == 2:
                    ready_bots.append(l_id)
            else:
                outputs[l_id].append(low)
                
            # Give high
            if h_type == 'bot':
                bots[h_id].append(high)
                if len(bots[h_id]) == 2:
                    ready_bots.append(h_id)
            else:
                outputs[h_id].append(high)
    
    return part1_ans, outputs

def part1():
    # Find bot comparing 61 and 17 (sorted: 17, 61)
    ans, _ = solve((17, 61))
    return ans

def part2():
    _, outputs = solve((17, 61))
    
    # "multiply together the values of one chip in each of outputs 0, 1, and 2"
    # We assume each output bin has at least one chip.
    if 0 in outputs and 1 in outputs and 2 in outputs:
        # Assuming one chip each, or just taking the first one?
        # "one chip in each". But puzzle implies outputs collect chips.
        # "output bin 0 contains a value-5 microchip..."
        v0 = outputs[0][0]
        v1 = outputs[1][0]
        v2 = outputs[2][0]
        return v0 * v1 * v2
    return None

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

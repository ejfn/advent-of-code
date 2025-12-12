
import sys
import os

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    initial_line = lines[0]
    initial_str = initial_line.split(': ')[1]
    
    state = set()
    for i, c in enumerate(initial_str):
        if c == '#':
            state.add(i)
            
    rules = {}
    for line in lines[1:]:
        parts = line.split(' => ')
        rules[parts[0]] = parts[1]
        
    return state, rules

def step(state, rules):
    if not state:
        return set()
        
    min_idx = min(state)
    max_idx = max(state)
    
    new_state = set()
    
    # We need to check 2 positions to the left of the leftmost plant
    # and 2 positions to the right of the rightmost plant
    # because ..#.. => # rules can create plants in empty space next to plants
    
    for i in range(min_idx - 2, max_idx + 3):
        pattern = ""
        for offset in range(-2, 3):
            if (i + offset) in state:
                pattern += "#"
            else:
                pattern += "."
        
        if pattern in rules and rules[pattern] == '#':
            new_state.add(i)
            
    return new_state

def simulate(initial_state, rules, generations):
    state = initial_state.copy()
    seen = {}
    
    # For Part 2 detection
    prev_sum = sum(state)
    diffs = []
    
    for gen in range(1, generations + 1):
        state = step(state, rules)
        current_sum = sum(state)
        diff = current_sum - prev_sum
        prev_sum = current_sum
        
        # Part 2 heuristic: if diff stabilizes, we can project
        diffs.append(diff)
        if len(diffs) > 100:
            last_100 = diffs[-100:]
            if all(d == last_100[0] for d in last_100):
                # Stable difference found!
                remaining_gens = generations - gen
                final_sum = current_sum + remaining_gens * diff
                return final_sum, state
                
    return sum(state), state

def part1(filename):
    state, rules = parse_input(filename)
    result, _ = simulate(state, rules, 20)
    return result

def part2(filename):
    state, rules = parse_input(filename)
    result, _ = simulate(state, rules, 50000000000)
    return result

def run_example():
    # Construct example input in memory or creating a temp file is hard
    # I'll just hardcode the logic test
    
    initial_str = "#..#.#..##......###...###"
    rules_list = [
        "...## => #", "..#.. => #", ".#... => #", ".#.#. => #", ".#.## => #",
        ".##.. => #", ".#### => #", "#.#.# => #", "#.### => #", "##.#. => #",
        "##.## => #", "###.. => #", "###.# => #", "####. => #"
    ]
    
    state = set()
    for i, c in enumerate(initial_str):
        if c == '#':
            state.add(i)
            
    rules = {}
    for r in rules_list:
        p = r.split(' => ')
        rules[p[0]] = p[1]
        
    # Example says 325 after 20 gens
    res, _ = simulate(state, rules, 20)
    print(f"Example result: {res} (Expected 325)")
    assert res == 325
    print("Example passed!")

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {part1(input_file)}")
    print(f"Part 2: {part2(input_file)}")

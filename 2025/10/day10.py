
import sys
import os
import re
import z3

def parse_input(content):
    machines = []
    # Line format: [diagram] (buttons...) {targets}
    # Example: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    
    lines = content.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
            
        # Parse Diagram
        diagram_match = re.search(r'\[([.#]+)\]', line)
        if not diagram_match:
            continue
        diagram_str = diagram_match.group(1)
        diagram = [1 if c == '#' else 0 for c in diagram_str]
        
        # Parse Targets
        targets_match = re.search(r'\{([\d,]+)\}', line)
        if not targets_match:
            continue
        targets = [int(x) for x in targets_match.group(1).split(',')]
        
        # Parse Buttons
        # Find all (numbers) groups
        # We can remove the diagram and targets parts to process buttons safely
        # Or just find all parenthesized groups
        
        # A clearer way: extract the middle part or use global findall
        # The buttons are between ] and {
        middle_part = line[line.find(']')+1 : line.find('{')]
        button_matches = re.findall(r'\(([\d,]+)\)', middle_part)
        buttons = []
        for b_str in button_matches:
            if not b_str.strip(): # handle () if possible? though puzzle says one or more schematics
                buttons.append([])
            else:
                buttons.append([int(x) for x in b_str.split(',')])
            
        machines.append({
            'diagram': diagram,
            'buttons': buttons,
            'targets': targets
        })
    return machines

def solve_part1_machine(machine):
    # Diagram is boolean target
    # Buttons toggle specified lights
    # x_i in {0, 1}
    # sum(button_effects) % 2 == diagram
    
    diagram = machine['diagram']
    buttons = machine['buttons']
    num_lights = len(diagram)
    num_buttons = len(buttons)
    
    opt = z3.Optimize()
    x = [z3.Int(f'x_{i}') for i in range(num_buttons)]
    
    for xi in x:
        opt.add(xi >= 0)
        opt.add(xi <= 1)
        
    for light_idx in range(num_lights):
        # build sum of x_i for buttons that affect this light
        terms = []
        for btn_idx, btn_affects in enumerate(buttons):
            if light_idx in btn_affects:
                terms.append(x[btn_idx])
        
        if not terms:
            current_val = 0
        else:
            current_val = z3.Sum(terms)
        
        # target is diagram[light_idx]
        # constraint: current_val % 2 == target
        opt.add(current_val % 2 == diagram[light_idx])
        
    # Minimize sum of presses
    opt.minimize(z3.Sum(x))
    
    if opt.check() == z3.sat:
        model = opt.model()
        return sum(model[xi].as_long() for xi in x)
    else:
        # Should not happen based on problem description
        return 0

def solve_part2_machine(machine):
    # Targets are integers
    # Buttons add 1 to specified counters
    # x_i >= 0
    # sum(button_effects) == targets
    
    targets = machine['targets']
    buttons = machine['buttons']
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    opt = z3.Optimize()
    x = [z3.Int(f'x_{i}') for i in range(num_buttons)]
    
    for xi in x:
        opt.add(xi >= 0)
        
    for counter_idx in range(num_counters):
        terms = []
        for btn_idx, btn_affects in enumerate(buttons):
            if counter_idx in btn_affects:
                terms.append(x[btn_idx])
        
        if not terms:
            # If no button affects this counter, and target is > 0, unsat
            # But we can add the constraint 0 == target
             opt.add(0 == targets[counter_idx])
        else:
            opt.add(z3.Sum(terms) == targets[counter_idx])
            
    opt.minimize(z3.Sum(x))
    
    if opt.check() == z3.sat:
        model = opt.model()
        return sum(model[xi].as_long() for xi in x)
    else:
        return 0

def part1(machines):
    total = 0
    for i, m in enumerate(machines):
        res = solve_part1_machine(m)
        total += res
    return total

def part2(machines):
    total = 0
    for i, m in enumerate(machines):
        res = solve_part2_machine(m)
        total += res
    return total

def parse_args():
    # Helper to support running specific parts if needed, though usually we run all
    pass

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        content = f.read()
        
    machines = parse_input(content)
    
    print("Part 1:", part1(machines))
    print("Part 2:", part2(machines))

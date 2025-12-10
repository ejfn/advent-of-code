
import sys
import os
import math
from collections import defaultdict, deque

def parse_input(data):
    reactions = {}
    for line in data.strip().split('\n'):
        inputs_str, output_str = line.split(' => ')
        
        inputs = []
        for item in inputs_str.split(', '):
            qty, chem = item.split(' ')
            inputs.append((int(qty), chem))
            
        qty_out, chem_out = output_str.split(' ')
        reactions[chem_out] = (int(qty_out), inputs)
        
    return reactions

def ore_required(fuel_amount, reactions):
    # Store leftover chemicals
    leftovers = defaultdict(int)
    
    # We need to produce fuel_amount FUEL
    needed = defaultdict(int)
    needed['FUEL'] = fuel_amount
    
    ore_count = 0
    
    # Needs topological sort? Or just iterative processing since it's a DAG?
    # Simple queue approach works if we process requirements.
    # Actually, iterative consumption.
    
    queue = ['FUEL']
    
    while queue:
        chem_needed = queue.pop(0) # Process next requirement
        
        # If we need ORE, we just count it? No, ORE is the base.
        # But 'needed' stores what we need to PRODUCE.
        # We handle ORE separately or treat it as base.
        
        qty_needed = needed[chem_needed]
        
        if chem_needed == 'ORE':
            ore_count += qty_needed
            needed[chem_needed] = 0 # consumed
            continue
            
        if qty_needed <= 0:
            continue
            
        # Check if we have leftovers
        if leftovers[chem_needed] >= qty_needed:
            leftovers[chem_needed] -= qty_needed
            needed[chem_needed] = 0
            continue
        else:
            # Use up leftovers
            qty_needed -= leftovers[chem_needed]
            leftovers[chem_needed] = 0
            needed[chem_needed] = qty_needed # Update needed, though we'll satisfy it now
            
        # Find reaction producing this chemical
        qty_produced, inputs = reactions[chem_needed]
        
        # Calculate how many times to run reaction
        multiplier = math.ceil(qty_needed / qty_produced)
        
        # Produce it
        total_produced = multiplier * qty_produced
        leftovers[chem_needed] += total_produced - qty_needed
        needed[chem_needed] = 0 # Satisfied
        
        # Add inputs to needed
        for input_qty, input_chem in inputs:
            total_input_needed = input_qty * multiplier
            
            # Optimization: if input is ORE, add directly to ore_count
            # Otherwise add to needed and queue
            if input_chem == 'ORE':
                ore_count += total_input_needed
            else:
                # If chemically already in queue?
                # Actually, standard approach:
                # We can't use a simple queue because we might add more needs later.
                # A topological sort is better, OR:
                # We can just sum up all needs for a chemical before processing it? 
                # Yes, if we process in topological order (reverse dependency).
                
                # But since we just want *any* valid path, this greedy approach with leftovers works 
                # IF the graph is a tree/DAG. It is.
                # BUT, order matters for reusing leftovers efficiently? 
                # Actually, "leftovers" are produced from excess.
                
                # Topological sort approach:
                # 1. Determine distances from FUEL
                # 2. Process in order of distance (furthest first?)
                pass
                
    # The simple queue matching above is WRONG because if we process A -> B and C -> B, 
    # and we process A then B, and then C adds more requirement for B, we might have wasted 
    # reactions or failed leftovers logic.
    # BETTER:
    # 1. Calculate full 'needed' amount.
    # 2. But we don't know needed amount without knowing multiples.
    
    # Recursive approach with leftovers state is common.
    return solve_ore_recursive(fuel_amount, reactions)

def solve_ore_recursive(fuel_amount, reactions):
    # State needs to persist
    leftovers = defaultdict(int)
    
    # Dictionary of required amounts
    orders = defaultdict(int)
    orders['FUEL'] = fuel_amount
    
    ore_count = 0
    
    # Use topological order to ensure we process all consumers before producers
    # Calculate topological order
    # Build graph
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    for chem in reactions:
        _, inputs = reactions[chem]
        for _, input_chem in inputs:
            if input_chem != 'ORE':
                adj[chem].append(input_chem) # chem depends on input_chem? 
                # No, we want to process consumers first.
                # FUEL consumes A. So A depends on FUEL?
                # We want to process FUEL, then A.
                # So edge FUEL -> A.
                in_degree[input_chem] += 1
    
    # But wait, inputs are "produced by ORE or other things".
    # Reaction: A + B -> C. To make C, we need A and B.
    # So C -> A, C -> B.
    
    # Initialize queue with 0 in-degree (FUEL should be one?)
    # FUEL is never an input to anything. So in_degree['FUEL'] should be 0.
    
    # Add all chemicals to in_degree map
    all_chems = set(reactions.keys())
    all_chems.add('ORE') # ORE is also a chem
    
    # Rebuild graph properly
    adj = defaultdict(list)
    in_degree = defaultdict(int) 
    
    # For every reaction Out -> In1, In2...
    # Edge Out -> In1, Out -> In2
    for out_chem, (_, inputs) in reactions.items():
        for _, in_chem in inputs:
            adj[out_chem].append(in_chem)
            in_degree[in_chem] += 1
            
    queue = deque([c for c in reactions if in_degree[c] == 0]) 
    # If FUEL is not in reactions keys (it is), and it's not input to anything, it starts 0.
    if 'FUEL' not in queue:
        # Should ideally be there. Let's force check
        if in_degree.get('FUEL', 0) == 0:
            queue.append('FUEL')

    # We only care about processing order.
    # If cyclic? Problem guarantees DAG.
    
    ore_needed = 0
    
    # Process order
    process_order = []
    
    # Kahn's algorithm
    while queue:
        u = queue.popleft()
        process_order.append(u)
        
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Process orders in topological order
    for chem in process_order:
        if chem == 'ORE':
            continue
            
        required = orders[chem]
        if required == 0:
            continue
            
        out_qty, inputs = reactions[chem]
        
        # We need 'required'.
        # We might have extra? No, 'orders' tracks exact needs.
        # But 'leftovers' isn't needed if we process in exact order?
        # WAIT. We can't strictly process exact needs if we produce in batches.
        # We produce in multiples of out_qty.
        
        mult = math.ceil(required / out_qty)
        produced = mult * out_qty
        # Surplus?
        # If we produce more than needed, that's fine, but the *next* dependency logic doesn't care about our surplus,
        # it cares about what WE need from THEM.
        
        for in_qty, in_chem in inputs:
            orders[in_chem] += in_qty * mult
            
    return orders['ORE']

def solve_part1(data):
    reactions = parse_input(data)
    return solve_ore_recursive(1, reactions)

def solve_part2(data):
    reactions = parse_input(data)
    target_ore = 1000000000000
    
    low = 1
    high = target_ore # Upper bound estimate
    
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        ore = solve_ore_recursive(mid, reactions)
        
        if ore <= target_ore:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    return ans

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data)) 

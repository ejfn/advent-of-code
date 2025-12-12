import sys
import os
import re
from collections import deque
from itertools import combinations, chain

# Floors are 0-indexed (0=1st floor, 3=4th floor)

def parse_input(lines):
    # Map element name to id
    elements = {}
    next_id = 0
    
    # Store initial positions: element_id -> [generator_floor, microchip_floor]
    # We will build this up.
    temp_positions = {}
    
    for floor_idx, line in enumerate(lines):
        # Extract generators
        # "a polonium generator"
        gens = re.findall(r'(\w+) generator', line)
        for g in gens:
            if g not in elements:
                elements[g] = next_id
                next_id += 1
            eid = elements[g]
            if eid not in temp_positions:
                temp_positions[eid] = [None, None]
            temp_positions[eid][0] = floor_idx
            
        # Extract microchips
        # "a thulium-compatible microchip"
        chips = re.findall(r'(\w+)-compatible microchip', line)
        for c in chips:
            if c not in elements:
                elements[c] = next_id
                next_id += 1
            eid = elements[c]
            if eid not in temp_positions:
                temp_positions[eid] = [None, None]
            temp_positions[eid][1] = floor_idx
            
    # Convert to list of pairs sorted by element ID (though sorting by value effectively canonicalizes)
    # The state we want is: (elevator_floor, tuple(sorted([(g_floor, m_floor) for each element])))
    # We don't care WHICH element is at (0,0) vs (1,1), just that THERE IS an element at those coords.
    pairs = []
    for eid in sorted(temp_positions.keys()):
        pairs.append(tuple(temp_positions[eid]))
    
    return 0, tuple(sorted(pairs))

def is_valid(pairs):
    # Check each floor safety
    # A floor is safe if:
    # No microchip is with another generator UNLESS its own generator is also there.
    # More simply: if a chip is on floor F, and its gen is NOT on floor F, then NO other gen can be on floor F.
    
    # Precompute generators on each floor
    gens_on_floor = [set() for _ in range(4)]
    chips_on_floor = [set() for _ in range(4)]
    
    for i, (g, m) in enumerate(pairs):
        gens_on_floor[g].add(i)
        chips_on_floor[m].add(i)
        
    for f in range(4):
        if not chips_on_floor[f] or not gens_on_floor[f]:
            continue
            
        # For each chip on this floor
        for chip_id in chips_on_floor[f]:
            # If its generator is not here
            if chip_id not in gens_on_floor[f]:
                # And there are ANY generators here (which we checked above with gens_on_floor[f])
                return False
    return True

def get_next_states(state):
    elevator, pairs = state
    next_states = []
    
    # Possible moves: 1 or 2 items from current floor
    # Identify indices of items on current floor
    # items are identified by (type, index_in_pairs)
    # type 0 = gen, type 1 = chip
    
    items_on_floor = []
    for i, (g, m) in enumerate(pairs):
        if g == elevator:
            items_on_floor.append((0, i)) # Generator i
        if m == elevator:
            items_on_floor.append((1, i)) # Microchip i
            
    possible_moves = []
    # 1 item
    for item in items_on_floor:
        possible_moves.append([item])
    # 2 items
    for item1, item2 in combinations(items_on_floor, 2):
        possible_moves.append([item1, item2])
        
    # Directions
    directions = []
    if elevator < 3: directions.append(1)
    if elevator > 0: directions.append(-1)
    
    # Heuristic optimization: Don't move 2 items down if we can move 1
    # Actually, we should try to move things UP.
    # If we are at floor F, and all floors below F are empty, don't move anything down.
    # Check if floors below are empty
    floors_below_empty = True
    for f in range(elevator):
        # check if any item is at floor f
        for g, m in pairs:
            if g == f or m == f:
                floors_below_empty = False
                break
        if not floors_below_empty:
            break
            
    for d in directions:
        next_floor = elevator + d
        if d == -1 and floors_below_empty:
            continue
            
        for move in possible_moves:
            # Create new pairs state
            # Tuples are immutable so we need to rebuild
            # It's easier to convert to list of lists, modify, then back to tuple of tuples
            
            # Optimization: don't move 1 item down if you can move 2?
            # Optimization: don't move 2 items up if you can move 1? -> No, moving 2 up is better.
            
            # Let's apply moves
            # We need to construct new state
            new_pairs_list = [list(p) for p in pairs]
            
            for type_idx, pair_idx in move:
                new_pairs_list[pair_idx][type_idx] = next_floor
                
            new_pairs = tuple(sorted(tuple(p) for p in new_pairs_list))
            
            if is_valid(new_pairs):
                next_states.append((next_floor, new_pairs))
                
    return next_states

def solve_bfs(initial_state):
    queue = deque([(0, initial_state)]) # steps, state
    visited = set([initial_state])
    
    # Target: all items on floor 3
    # Target state shape: (3, ((3,3), (3,3), ...))
    target_pairs = tuple((3, 3) for _ in initial_state[1])
    # Note: target elevator floor is 3. 
    # Actually elevator must be at 3 too if everything is at 3.
    
    while queue:
        steps, state = queue.popleft()
        elevator, pairs = state
        
        if pairs == target_pairs and elevator == 3:
            return steps
        
        for next_state in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((steps + 1, next_state))
                
    return -1

def part1():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    initial_state = parse_input(lines)
    return solve_bfs(initial_state)

def part2():
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    initial_elevator, initial_pairs = parse_input(lines)
    
    # Part 2: Add 2 pairs at floor 0 (1st floor)
    # Elerium generator, Elerium-compatible microchip
    # Dilithium generator, Dilithium-compatible microchip
    extra_pairs = ((0, 0), (0, 0))
    
    new_pairs = tuple(sorted(initial_pairs + extra_pairs))
    
    return solve_bfs((initial_elevator, new_pairs))

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())


import sys
import os
import copy
from collections import deque

class Unit:
    def __init__(self, x, y, team, hp=200, attack_power=3, uid=0):
        self.x = x
        self.y = y
        self.team = team # 'E' or 'G'
        self.hp = hp
        self.attack_power = attack_power
        self.uid = uid
        
    def __repr__(self):
        return f"{self.team}({self.hp}) at {self.x},{self.y}"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

class Battle:
    def __init__(self, grid_lines, elf_power=3):
        self.height = len(grid_lines)
        self.width = len(grid_lines[0])
        self.walls = set()
        self.units = []
        uid_counter = 0
        
        for y, line in enumerate(grid_lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.walls.add((x, y))
                elif char in 'GE':
                    power = elf_power if char == 'E' else 3
                    self.units.append(Unit(x, y, char, attack_power=power, uid=uid_counter))
                    uid_counter += 1
                    
    def is_free(self, x, y, exclude_unit=None):
        if (x, y) in self.walls:
            return False
        for unit in self.units:
            if unit.hp > 0 and (unit.x, unit.y) == (x, y) and unit != exclude_unit:
                return False
        return True

    def get_adj(self, x, y):
        # Reading order: Up, Left, Right, Down
        # Note: (0,0) is top-left.
        # Up: y-1, Left: x-1, Right: x+1, Down: y+1
        # Reading order for *adjacent* selection is also important.
        # "adjacent target ... first in reading order"
        # Reading order of positions is (y, x).
        # Potentially adjacent cells: (x, y-1), (x-1, y), (x+1, y), (x, y+1)
        # These are already sorted in reading order!
        candidates = [
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)
        ]
        return candidates

    def run_round(self):
        # Sort units by reading order
        self.units.sort()
        
        for unit in self.units:
            if unit.hp <= 0:
                continue
                
            # Check if targets exist
            targets = [u for u in self.units if u.team != unit.team and u.hp > 0]
            if not targets:
                return False # Combat ends
            
            # Attack if already in range
            if self.attack(unit):
                continue
                
            # Move
            start_pos = (unit.x, unit.y)
            
            # Identify all squares in range of targets
            in_range = set()
            for t in targets:
                for ax, ay in self.get_adj(t.x, t.y):
                    if self.is_free(ax, ay, exclude_unit=unit):
                        in_range.add((ax, ay))
            
            if not in_range:
                continue
                
            # BFS to find reachable squares and their distances
            # We need shortest path to any in_range square.
            # Tie breakers: 1. fewest steps, 2. reading order of destination
            
            queue = deque([(unit.x, unit.y, 0)])
            visited = set([(unit.x, unit.y)])
            dists = {}
            
            # Find all reachable info
            reachable_in_range = []
            min_dist = float('inf')
            
            # Simple BFS to flood fill
            while queue:
                cx, cy, d = queue.popleft()
                
                if d > min_dist:
                    # We can stop if we went deeper than found solutions
                    # (Because BFS guarantees finding shortest first, but we need to find ALL at that shortest dist)
                    # Actually, since we process level by level, if we pop something > min_dist, we are done looking for destinations
                    break
                
                if (cx, cy) in in_range:
                    if d < min_dist:
                        min_dist = d
                    if d == min_dist:
                        reachable_in_range.append((cx, cy))
                
                for nx, ny in self.get_adj(cx, cy):
                    if (nx, ny) not in visited and self.is_free(nx, ny):
                        visited.add((nx, ny))
                        queue.append((nx, ny, d + 1))
                        dists[(nx, ny)] = d + 1
            
            if not reachable_in_range:
                continue
                
            # Choose destination: min dist (already handled), then reading order
            reachable_in_range.sort(key=lambda p: (p[1], p[0]))
            dest = reachable_in_range[0]
            
            # Determine step: shortest path to dest.
            # If multiple steps, choose reading order.
            # We can do this by checking neighbors of unit: which one leads to dest with dist - 1?
            
            # But wait, we need the distance from valid neighbor to dest.
            # We can do a reverse BFS from dest to unit to find the distances.
            # Or run BFS from each neighbor to dest (ok since grid is 32x32, small enough)
            
            step_chosen = None
            min_step_dist = float('inf')
            
            for nx, ny in self.get_adj(unit.x, unit.y):
                if not self.is_free(nx, ny):
                    continue
                    
                # Calculate dist from (nx, ny) to dest
                # Use BFS
                q2 = deque([(nx, ny, 0)])
                v2 = set([(nx, ny)])
                found = False
                this_dist = float('inf')
                
                while q2:
                    curr_x, curr_y, d2 = q2.popleft()
                    if (curr_x, curr_y) == dest:
                        this_dist = d2
                        found = True
                        break
                    
                    for nnx, nny in self.get_adj(curr_x, curr_y):
                        if (nnx, nny) not in v2 and self.is_free(nnx, nny):
                            v2.add((nnx, nny))
                            q2.append((nnx, nny, d2 + 1))
                            
                if found:
                    if this_dist < min_step_dist:
                        min_step_dist = this_dist
                        step_chosen = (nx, ny)
                    # Ties in min_step_dist are handled by the order of get_adj (reading order) 
                    # effectively? 
                    # get_adj returns reading order: Up, Left, Right, Down.
                    # Loop processes in reading order.
                    # "the unit chooses the step which is first in reading order"
                    # Yes, if we find a strictly better dist, we update. 
                    # If equal dist, we keep the first one encountered (smaller in reading order).
                    # Wait, logic above "if this_dist < min_step_dist" handles strict inequality.
                    # This means we prefer earlier ones if strict inequality fails.
                    # Correct.
            
            if step_chosen:
                unit.x, unit.y = step_chosen
                
            # After move, try to attack
            self.attack(unit)
            
        return True # Round completed fully

    def attack(self, unit):
        targets = []
        for nx, ny in self.get_adj(unit.x, unit.y):
            # Check for enemy
            for other in self.units:
                if other.hp > 0 and other.team != unit.team and (other.x, other.y) == (nx, ny):
                    targets.append(other)
        
        if not targets:
            return False
            
        # Select target: fewest HP, then reading order
        targets.sort(key=lambda u: (u.hp, u.y, u.x))
        victim = targets[0]
        
        victim.hp -= unit.attack_power
        return True

    def calculate_outcome(self, rounds):
        total_hp = sum(u.hp for u in self.units if u.hp > 0)
        return rounds * total_hp

def solve_part1(input_file):
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    
    battle = Battle(lines)
    rounds = 0
    while True:
        if not battle.run_round():
            break
        rounds += 1
    
    # The loop breaks when a round is *incomplete*.
    # The problem says: "the number of full rounds that were completed"
    # If run_round() returns False, it means inside the loop a unit found no targets.
    # So that round didn't complete. `rounds` counter counts full rounds.
    # However, if run_round() returns False, we must ensure we processed untill the end?
    # No, "run_round" executes turns. If a unit finds no targets, combat ends *immediately*.
    # My run_round returns False immediately.
    # So `rounds` will be the number of full rounds.
    
    return battle.calculate_outcome(rounds)

def solve_part2(input_file):
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        
    # Binary search or linear search for power?
    # "find the outcome ... such that no Elves die?"
    # Just linear search from 4 upwards.
    
    power = 4
    while True:
        battle = Battle(lines, elf_power=power)
        elf_count_start = len([u for u in battle.units if u.team == 'E'])
        
        rounds = 0
        elf_died = False
        while True:
            # We need to detect elf death immediately to abort early optimization
            # run_round handles logic, but let's check between turns?
            # Or just check after round.
            # Actually, `run_round` processes all units. If an elf dies during a round, 
            # we can check at end of round (or modify run_round to return status).
            
            # To be strict: "Elves must not die".
            if not battle.run_round():
                # Game over
                break
            
            # Check if any elf died
            current_elves = len([u for u in battle.units if u.team == 'E' and u.hp > 0])
            if current_elves < elf_count_start:
                elf_died = True
                break
                
            rounds += 1
            
        # Final check
        current_elves = len([u for u in battle.units if u.team == 'E' and u.hp > 0])
        if not elf_died and current_elves == elf_count_start:
            # All elves survived and we finished
            return battle.calculate_outcome(rounds)
            
        power += 1

def run_example():
    ex1 = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
    # Expected: 27730
    
    # I'll create a temp file for consistency
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(ex1)
        tmp_path = tmp.name
        
    res = solve_part1(tmp_path)
    print(f"Example 1 Result: {res} (Expected 27730)")
    os.remove(tmp_path)
    assert res == 27730
    
if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

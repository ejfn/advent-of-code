
import sys
import re
import copy
import os

class Group:
    def __init__(self, army_name, group_id, units, hp, damage, damage_type, initiative, weaknesses, immunities):
        self.army = army_name
        self.id = group_id
        self.units = units
        self.hp = hp
        self.damage = damage
        self.damage_type = damage_type
        self.initiative = initiative
        self.weaknesses = set(weaknesses)
        self.immunities = set(immunities)
        
        self.target = None # Who am I attacking?
        self.is_targeted = False # Am I targeted by someone?
        self.boost = 0 # For Part 2

    @property
    def effective_power(self):
        return self.units * (self.damage + self.boost)

    def calc_damage_to(self, defender):
        if self.damage_type in defender.immunities:
            return 0
        damage = self.effective_power
        if self.damage_type in defender.weaknesses:
            damage *= 2
        return damage

    def __repr__(self):
        return f"{self.army} {self.id} ({self.units} units)"

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    groups = []
    current_army = ""
    group_counter = 1
    
    # Regex for main line
    # 17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
    # Note: the (weak/immune) part is optional
    
    # We can split by " units each with " etc?
    # Or strict regex.
    # The parenthetical group is tricky because it might not exist.
    
    regex = re.compile(r"(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)")
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.endswith(':'):
            current_army = line[:-1]
            group_counter = 1
            continue
            
        m = regex.match(line)
        if m:
            units = int(m.group(1))
            hp = int(m.group(2))
            props_str = m.group(3)
            damage = int(m.group(4))
            damage_type = m.group(5)
            initiative = int(m.group(6))
            
            weaknesses = []
            immunities = []
            
            if props_str:
                # Remove parens and trailing space "with " is outside group but regex logic
                # Regex group 3 includes trailing space if matched?
                # "weak to radiation) "
                content = props_str.strip()[1:-1] # Remove parens
                parts = content.split('; ')
                for p in parts:
                    if p.startswith("weak to "):
                        weaknesses = p[8:].split(', ')
                    elif p.startswith("immune to "):
                        immunities = p[10:].split(', ')
                        
            groups.append(Group(current_army, group_counter, units, hp, damage, damage_type, initiative, weaknesses, immunities))
            group_counter += 1
            
    return groups

def fight_round(groups):
    # 1. Target Selection
    # Sort attackers: Eff Power desc, Init desc
    groups.sort(key=lambda g: (-g.effective_power, -g.initiative))
    
    # Reset targeting state
    for g in groups:
        g.target = None
        g.is_targeted = False
        
    # We need to process selection carefully.
    # Potential targets are enemies not yet targeted.
    
    # To properly handle the "is_targeted" status during selection:
    # We iterate groups in priority order.
    # For each group, we find best target among UNTARGETED enemies.
    # Then mark chosen target as targeted.
    # BUT "Defending groups can only be chosen as a target by one attacking group."
    # Yes, so we need to track `targeted_groups` set for THIS round.
    
    targeted_ids = set() # (army, id)
    
    for attacker in groups:
        if attacker.units <= 0: continue
        
        candidates = []
        for defender in groups:
            if defender.units <= 0: continue
            if defender.army == attacker.army: continue
            if (defender.army, defender.id) in targeted_ids: continue
            
            dmg = attacker.calc_damage_to(defender)
            if dmg == 0: continue
            
            candidates.append((dmg, defender.effective_power, defender.initiative, defender))
            
        if candidates:
            # Sort candidates: Damage desc, EffPower desc, Init desc
            candidates.sort(key=lambda x: (-x[0], -x[1], -x[2]))
            best_target = candidates[0][3]
            attacker.target = best_target
            targeted_ids.add((best_target.army, best_target.id))
            
    # 2. Attacking
    # Sort by Initiative desc
    groups.sort(key=lambda g: -g.initiative)
    
    total_killed = 0
    
    for attacker in groups:
        if attacker.units <= 0: continue
        defender = attacker.target
        if not defender: continue
        if defender.units <= 0: continue # Already dead this round (killed by higher init)
        
        dmg = attacker.calc_damage_to(defender)
        killed = dmg // defender.hp
        killed = min(killed, defender.units)
        
        defender.units -= killed
        total_killed += killed
        
    return total_killed

def simulate(groups, boost=0):
    # Apply boost to Immune System
    groups = copy.deepcopy(groups)
    for g in groups:
        if g.army == "Immune System":
            g.boost = boost
            
    while True:
        # Check winning condition
        immune_alive = any(g.units > 0 for g in groups if g.army == "Immune System")
        infection_alive = any(g.units > 0 for g in groups if g.army == "Infection")
        
        if not immune_alive:
            return "Infection", sum(g.units for g in groups if g.army == "Infection")
        if not infection_alive:
            return "Immune System", sum(g.units for g in groups if g.army == "Immune System")
            
        killed = fight_round(groups)
        if killed == 0:
            # Stalemate
            return "Draw", 0 # No damage dealt, infinite loop
            
def solve_part1(filename):
    groups = parse_input(filename)
    winner, units = simulate(groups)
    return units

def solve_part2(filename):
    groups = parse_input(filename)
    
    # Linear search for boost
    boost = 1
    while True:
        winner, units = simulate(groups, boost)
        # print(f"Boost {boost}: Winner {winner}, Units {units}")
        if winner == "Immune System":
            return units
        boost += 1

def run_example():
    ex = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
    
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(ex)
        tmp_name = tmp.name
        
    try:
        p1 = solve_part1(tmp_name)
        print(f"Example Part 1: {p1} (Expected 5216)")
        assert p1 == 5216
        
        # Example Part 2 (boost 1570 is minimal for Immune System to win with 51 units left)
        # Wait, description says: "With a boost of 1570, the Immune System wins with 51 units left."
        p2 = solve_part2(tmp_name)
        print(f"Example Part 2: {p2} (Expected 51)")
        assert p2 == 51
        
        print("Examples passed!")
    finally:
        os.remove(tmp_name)

if __name__ == '__main__':
    run_example()
    
    import os
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")

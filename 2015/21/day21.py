import os
import sys
from itertools import combinations

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')
    boss = {}
    for line in lines:
        key, val = line.split(': ')
        boss[key] = int(val)
    return boss

# Shop items: (cost, damage, armor)
WEAPONS = [
    (8, 4, 0),   # Dagger
    (10, 5, 0),  # Shortsword
    (25, 6, 0),  # Warhammer
    (40, 7, 0),  # Longsword
    (74, 8, 0),  # Greataxe
]

ARMOR = [
    (0, 0, 0),   # No armor
    (13, 0, 1),  # Leather
    (31, 0, 2),  # Chainmail
    (53, 0, 3),  # Splintmail
    (75, 0, 4),  # Bandedmail
    (102, 0, 5), # Platemail
]

RINGS = [
    (0, 0, 0),   # No ring
    (25, 1, 0),  # Damage +1
    (50, 2, 0),  # Damage +2
    (100, 3, 0), # Damage +3
    (20, 0, 1),  # Defense +1
    (40, 0, 2),  # Defense +2
    (80, 0, 3),  # Defense +3
]

def player_wins(player_hp, player_damage, player_armor, boss_hp, boss_damage, boss_armor):
    player_dmg = max(1, player_damage - boss_armor)
    boss_dmg = max(1, boss_damage - player_armor)
    
    player_turns = (boss_hp + player_dmg - 1) // player_dmg
    boss_turns = (player_hp + boss_dmg - 1) // boss_dmg
    
    return player_turns <= boss_turns

def all_loadouts():
    for weapon in WEAPONS:
        for armor in ARMOR:
            # 0, 1, or 2 rings
            for ring_combo in [[], *combinations(RINGS[1:], 1), *combinations(RINGS[1:], 2)]:
                cost = weapon[0] + armor[0] + sum(r[0] for r in ring_combo)
                damage = weapon[1] + armor[1] + sum(r[1] for r in ring_combo)
                arm = weapon[2] + armor[2] + sum(r[2] for r in ring_combo)
                yield cost, damage, arm

def part1(boss):
    min_cost = float('inf')
    for cost, damage, armor in all_loadouts():
        if player_wins(100, damage, armor, boss['Hit Points'], boss['Damage'], boss['Armor']):
            min_cost = min(min_cost, cost)
    return min_cost

def part2(boss):
    max_cost = 0
    for cost, damage, armor in all_loadouts():
        if not player_wins(100, damage, armor, boss['Hit Points'], boss['Damage'], boss['Armor']):
            max_cost = max(max_cost, cost)
    return max_cost

if __name__ == "__main__":
    boss = load_input()
    print("Part 1:", part1(boss))
    print("Part 2:", part2(boss))

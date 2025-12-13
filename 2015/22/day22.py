import os
import sys
from heapq import heappush, heappop

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        lines = f.read().strip().split('\n')
    boss = {}
    for line in lines:
        key, val = line.split(': ')
        boss[key] = int(val)
    return boss

# Spells: (cost, damage, heal, effect)
SPELLS = {
    'missile': (53, 4, 0, None),
    'drain': (73, 2, 2, None),
    'shield': (113, 0, 0, ('shield', 6)),
    'poison': (173, 0, 0, ('poison', 6)),
    'recharge': (229, 0, 0, ('recharge', 5)),
}

def apply_effects(state):
    player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer = state
    armor = 0
    if shield_timer > 0:
        armor = 7
        shield_timer -= 1
    if poison_timer > 0:
        boss_hp -= 3
        poison_timer -= 1
    if recharge_timer > 0:
        player_mana += 101
        recharge_timer -= 1
    return (player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer), armor

def solve(boss, hard_mode=False):
    # State: (mana_spent, player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer)
    initial = (0, 50, 500, boss['Hit Points'], 0, 0, 0)
    pq = [initial]
    visited = set()
    
    while pq:
        mana_spent, player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer = heappop(pq)
        
        state_key = (player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer)
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Hard mode: player loses 1 HP at start of their turn
        if hard_mode:
            player_hp -= 1
            if player_hp <= 0:
                continue
        
        # Apply effects at start of player turn
        state = (player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer)
        state, _ = apply_effects(state)
        player_hp, player_mana, boss_hp, shield_timer, poison_timer, recharge_timer = state
        
        if boss_hp <= 0:
            return mana_spent
        
        # Try each spell
        for spell_name, (cost, damage, heal, effect) in SPELLS.items():
            if player_mana < cost:
                continue
            # Can't cast if effect already active
            if effect:
                eff_name, eff_dur = effect
                if eff_name == 'shield' and shield_timer > 0:
                    continue
                if eff_name == 'poison' and poison_timer > 0:
                    continue
                if eff_name == 'recharge' and recharge_timer > 0:
                    continue
            
            new_mana = player_mana - cost
            new_boss_hp = boss_hp - damage
            new_player_hp = player_hp + heal
            new_shield = shield_timer
            new_poison = poison_timer
            new_recharge = recharge_timer
            
            if effect:
                eff_name, eff_dur = effect
                if eff_name == 'shield':
                    new_shield = eff_dur
                elif eff_name == 'poison':
                    new_poison = eff_dur
                elif eff_name == 'recharge':
                    new_recharge = eff_dur
            
            # Boss turn
            state = (new_player_hp, new_mana, new_boss_hp, new_shield, new_poison, new_recharge)
            state, armor = apply_effects(state)
            new_player_hp, new_mana, new_boss_hp, new_shield, new_poison, new_recharge = state
            
            if new_boss_hp <= 0:
                return mana_spent + cost
            
            # Boss attacks
            boss_dmg = max(1, boss['Damage'] - armor)
            new_player_hp -= boss_dmg
            
            if new_player_hp > 0:
                heappush(pq, (mana_spent + cost, new_player_hp, new_mana, new_boss_hp, new_shield, new_poison, new_recharge))
    
    return None

def part1(boss):
    return solve(boss, hard_mode=False)

def part2(boss):
    return solve(boss, hard_mode=True)

if __name__ == "__main__":
    boss = load_input()
    print("Part 1:", part1(boss))
    print("Part 2:", part2(boss))

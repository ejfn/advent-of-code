import os
import sys
import re
from itertools import product

def load_input():
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        return [line.strip() for line in f if line.strip()]

def parse_ingredients(lines):
    ingredients = []
    for line in lines:
        m = re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
        ingredients.append({
            'name': m.group(1),
            'capacity': int(m.group(2)),
            'durability': int(m.group(3)),
            'flavor': int(m.group(4)),
            'texture': int(m.group(5)),
            'calories': int(m.group(6))
        })
    return ingredients

def calculate_score(ingredients, amounts):
    capacity = sum(ing['capacity'] * amt for ing, amt in zip(ingredients, amounts))
    durability = sum(ing['durability'] * amt for ing, amt in zip(ingredients, amounts))
    flavor = sum(ing['flavor'] * amt for ing, amt in zip(ingredients, amounts))
    texture = sum(ing['texture'] * amt for ing, amt in zip(ingredients, amounts))
    
    capacity = max(0, capacity)
    durability = max(0, durability)
    flavor = max(0, flavor)
    texture = max(0, texture)
    
    return capacity * durability * flavor * texture

def calculate_calories(ingredients, amounts):
    return sum(ing['calories'] * amt for ing, amt in zip(ingredients, amounts))

def combinations(n, total):
    """Generate all ways to distribute 'total' among 'n' items."""
    if n == 1:
        yield (total,)
    else:
        for i in range(total + 1):
            for rest in combinations(n - 1, total - i):
                yield (i,) + rest

def part1(lines):
    ingredients = parse_ingredients(lines)
    return max(calculate_score(ingredients, combo) for combo in combinations(len(ingredients), 100))

def part2(lines):
    ingredients = parse_ingredients(lines)
    max_score = 0
    for combo in combinations(len(ingredients), 100):
        if calculate_calories(ingredients, combo) == 500:
            score = calculate_score(ingredients, combo)
            max_score = max(max_score, score)
    return max_score

if __name__ == "__main__":
    data = load_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))

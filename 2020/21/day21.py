import os
import sys
from typing import Dict, List, Set, Tuple

Food = Tuple[Set[str], Set[str]]


def parse(data: str) -> List[Food]:
    foods: List[Food] = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        ingredients_part, allergens_part = line.split(' (contains ')
        ingredients = set(ingredients_part.split())
        allergens = set(allergen.strip() for allergen in allergens_part[:-1].split(','))
        foods.append((ingredients, allergens))
    return foods


def determine_allergens(foods: List[Food]) -> Tuple[Dict[str, Set[str]], Set[str]]:
    allergen_candidates: Dict[str, Set[str]] = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in allergen_candidates:
                allergen_candidates[allergen] &= ingredients
            else:
                allergen_candidates[allergen] = set(ingredients)
    possible_with_allergens = set().union(*allergen_candidates.values()) if allergen_candidates else set()
    return allergen_candidates, possible_with_allergens


def part1(data: str) -> int:
    foods = parse(data)
    _, possibly_allergenic = determine_allergens(foods)
    safe_count = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient not in possibly_allergenic:
                safe_count += 1
    return safe_count


def resolve_allergens(allergen_candidates: Dict[str, Set[str]]) -> Dict[str, str]:
    resolved: Dict[str, str] = {}
    candidates = {k: set(v) for k, v in allergen_candidates.items()}
    while candidates:
        found = [(allergen, next(iter(ings))) for allergen, ings in candidates.items() if len(ings) == 1]
        if not found:
            raise RuntimeError('Cannot resolve allergens uniquely')
        for allergen, ingredient in found:
            resolved[allergen] = ingredient
            del candidates[allergen]
            for other in candidates.values():
                other.discard(ingredient)
    return resolved


def part2(data: str) -> str:
    foods = parse(data)
    candidates, _ = determine_allergens(foods)
    resolved = resolve_allergens(candidates)
    dangerous = [ingredient for allergen, ingredient in sorted(resolved.items())]
    return ','.join(dangerous)


def read_input() -> str:
    path = os.path.join(sys.path[0], 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def run_example() -> None:
    example = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
    print("Example Part 1:", part1(example))  # Expected 5
    print("Example Part 2:", part2(example))  # Expected mxmxvkd,sqjhc,fvjkl


if __name__ == '__main__':
    data = read_input()
    print(part1(data))
    print(part2(data))

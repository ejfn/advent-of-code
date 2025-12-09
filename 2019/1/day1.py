
import os
import sys

def calculate_fuel(mass):
    return (mass // 3) - 2

def part1(lines):
    total_fuel = 0
    for line in lines:
        if not line:
            continue
        mass = int(line)
        total_fuel += calculate_fuel(mass)
    return total_fuel


def calculate_fuel_recursive(mass):
    total = 0
    while True:
        fuel = (mass // 3) - 2
        if fuel <= 0:
            break
        total += fuel
        mass = fuel
    return total

def part2(lines):
    total_fuel = 0
    for line in lines:
        if not line:
            continue
        mass = int(line)
        total_fuel += calculate_fuel_recursive(mass)
    return total_fuel

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Run examples from problem description
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583
    
    assert calculate_fuel_recursive(14) == 2
    assert calculate_fuel_recursive(1969) == 966
    assert calculate_fuel_recursive(100756) == 50346

    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")

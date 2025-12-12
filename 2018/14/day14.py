
import sys
import os

def solve_part1(input_val):
    target = int(input_val)
    recipes = [3, 7]
    p1 = 0
    p2 = 1
    
    # We need n + 10 recipes
    while len(recipes) < target + 10:
        s = recipes[p1] + recipes[p2]
        if s >= 10:
            recipes.append(s // 10)
            recipes.append(s % 10)
        else:
            recipes.append(s)
            
        p1 = (p1 + 1 + recipes[p1]) % len(recipes)
        p2 = (p2 + 1 + recipes[p2]) % len(recipes)
        
    return "".join(map(str, recipes[target : target+10]))

def solve_part2(input_val):
    # This is speculative until I see Part 2, but very likely based on pattern
    # Find sequence input_val in recipes
    target_seq = [int(c) for c in input_val]
    len_target = len(target_seq)
    
    recipes = [3, 7]
    p1 = 0
    p2 = 1
    
    # Efficient search?
    # Since we append 1 or 2 digits, we check the tail after append
    
    # Optimization: pre-calculate target_seq if comparing often?
    
    while True:
        s = recipes[p1] + recipes[p2]
        if s >= 10:
            recipes.append(s // 10)
            if recipes[-len_target:] == target_seq:
                return len(recipes) - len_target
            recipes.append(s % 10)
            if recipes[-len_target:] == target_seq:
                return len(recipes) - len_target
        else:
            recipes.append(s)
            if recipes[-len_target:] == target_seq:
                return len(recipes) - len_target
            
        p1 = (p1 + 1 + recipes[p1]) % len(recipes)
        p2 = (p2 + 1 + recipes[p2]) % len(recipes)
        
        # Safety break?
        if len(recipes) > 30000000: # 30 million
            # Just to prevent infinite loop if my guess is wrong
            break

    return None

def part1(input_text):
    return solve_part1(input_text)

def part2(input_text):
    return solve_part2(input_text)

def run_example():
    print("Running examples...")
    assert solve_part1("9") == "5158916779"
    assert solve_part1("5") == "0124515891"
    assert solve_part1("18") == "9251071085"
    assert solve_part1("2018") == "5941429882"
    print("Part 1 Examples Passed")
    
    # Speculative Part 2 examples
    # The problem says "After 5 recipes... 0124515891"
    # If the question is "How many recipes to left of 51589", answer should be 9
    assert solve_part2("51589") == 9
    assert solve_part2("01245") == 5
    assert solve_part2("92510") == 18
    assert solve_part2("59414") == 2018
    print("Part 2 Examples Passed")

if __name__ == '__main__':
    run_example()
    
    with open(os.path.join(sys.path[0], 'input.txt')) as f:
        input_text = f.read().strip()
    
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")

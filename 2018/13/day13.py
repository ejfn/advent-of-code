
import sys
import os

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # ^, v, <, >
        self.turn_count = 0  # 0: left, 1: straight, 2: right
        self.crashed = False

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, {self.direction})"

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    grid = []
    carts = []
    
    # Pad lines to max length just in case
    max_len = max(len(l) for l in lines)
    
    for y, line in enumerate(lines):
        row = list(line.ljust(max_len))
        for x, char in enumerate(row):
            if char in '^v<>':
                carts.append(Cart(x, y, char))
                # Replace cart on track with correct track piece
                # Assuming simple track logic underneath
                if char in '^v':
                    row[x] = '|'
                elif char in '<>':
                    row[x] = '-'
        grid.append(row)
        
    return grid, carts

def turn_left(direction):
    dirs = ['^', '<', 'v', '>']
    return dirs[(dirs.index(direction) + 1) % 4]

def turn_right(direction):
    dirs = ['^', '<', 'v', '>']
    return dirs[(dirs.index(direction) - 1) % 4]

def move_cart(cart, grid):
    dx, dy = 0, 0
    if cart.direction == '^': dy = -1
    elif cart.direction == 'v': dy = 1
    elif cart.direction == '<': dx = -1
    elif cart.direction == '>': dx = 1
    
    cart.x += dx
    cart.y += dy
    
    track = grid[cart.y][cart.x]
    
    if track == '+':
        if cart.turn_count == 0: # Left
            cart.direction = turn_left(cart.direction)
        elif cart.turn_count == 2: # Right
            cart.direction = turn_right(cart.direction)
        # 1 is straight (no change)
        cart.turn_count = (cart.turn_count + 1) % 3
        
    elif track == '/':
        if cart.direction == '^': cart.direction = '>'
        elif cart.direction == 'v': cart.direction = '<'
        elif cart.direction == '<': cart.direction = 'v'
        elif cart.direction == '>': cart.direction = '^'
        
    elif track == '\\':
        if cart.direction == '^': cart.direction = '<'
        elif cart.direction == 'v': cart.direction = '>'
        elif cart.direction == '<': cart.direction = '^'
        elif cart.direction == '>': cart.direction = 'v'
        
    # | and - don't change direction given valid movement

def solve(filename, part2=False):
    grid, carts = parse_input(filename)
    
    tick = 0
    while True:
        tick += 1
        carts.sort()
        
        # Check for crashes during movement
        for i, cart in enumerate(carts):
            if cart.crashed:
                continue
                
            move_cart(cart, grid)
            
            # Check collision with any other cart
            for other in carts:
                if other is not cart and not other.crashed:
                    if other.x == cart.x and other.y == cart.y:
                        # CRASH
                        if not part2:
                            return f"{cart.x},{cart.y}"
                        
                        cart.crashed = True
                        other.crashed = True
                        # Don't break immediately, handle other crashes? 
                        # Problem says "removes them".
                        # Check logic: "Eventually, only one cart remains"
        
        # Remove crashed carts for Part 2
        if part2:
            carts = [c for c in carts if not c.crashed]
            if len(carts) == 1:
                return f"{carts[0].x},{carts[0].y}"
            if len(carts) == 0:
                # Should not happen typically unless even number crash into each other last
                 return "0,0" # Error?

def part1(filename):
    return solve(filename, part2=False)

def part2(filename):
    return solve(filename, part2=True)

def run_example():
    # Example 1
    ex1 = """/->-\\
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
\\------/"""
    
    # Needs to be written to file to use parse_input or refactor
    # I'll refactor parse_input to take lines? No, file is fine.
    # I'll write to a temp file
    
    with open('example_input.txt', 'w') as f:
        f.write(ex1)
        
    res = solve('example_input.txt')
    print(f"Example 1 Result: {res} (Expected 7,3)")
    assert res == "7,3"
    
    # Part 2 Example
    ex2 = """/>-<\\
|   |
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/"""
    with open('example_input_2.txt', 'w') as f:
        f.write(ex2)
        
    res2 = solve('example_input_2.txt', part2=True)
    print(f"Example 2 Result: {res2} (Expected 6,4)")
    assert res2 == "6,4"
    
    print("Examples passed!")
    
    # Cleanup
    if os.path.exists('example_input.txt'): os.remove('example_input.txt')
    if os.path.exists('example_input_2.txt'): os.remove('example_input_2.txt')

if __name__ == '__main__':
    run_example()
    
    input_file = os.path.join(sys.path[0], 'input.txt')
    print(f"Part 1: {part1(input_file)}")
    print(f"Part 2: {part2(input_file)}")

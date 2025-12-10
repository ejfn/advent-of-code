
import sys
import os

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

def parse_layers(data):
    layers = []
    for i in range(0, len(data), LAYER_SIZE):
        layers.append(data[i:i+LAYER_SIZE])
    return layers

def solve_part1(data):
    layers = parse_layers(data)
    
    min_zeros = float('inf')
    result = 0
    
    for layer in layers:
        zeros = layer.count('0')
        if zeros < min_zeros:
            min_zeros = zeros
            result = layer.count('1') * layer.count('2')
            
    return result

def solve_part2(data):
    # Likely rendering
    # 0 = Black, 1 = White, 2 = Transparent
    layers = parse_layers(data)
    final_image = ['2'] * LAYER_SIZE
    
    for i in range(LAYER_SIZE):
        for layer in layers:
            pixel = layer[i]
            if pixel != '2':
                final_image[i] = pixel
                break
    
    # Render
    output = []
    for i in range(0, LAYER_SIZE, WIDTH):
        row = final_image[i:i+WIDTH]
        # Replace 0 with ' ' and 1 with '#' for readability
        rendered_row = ''.join(['#' if p == '1' else ' ' for p in row])
        output.append(rendered_row)
        
    return '\n'.join(output)

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1(data))
    print("Part 2:")
    print(solve_part2(data))

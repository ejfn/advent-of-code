
import sys
import os

def parse_input(data):
    return data.strip().split('\n')

def deal_into_new_stack(deck):
    return deck[::-1]

def cut_n(deck, n):
    return deck[n:] + deck[:n]

def deal_with_increment_n(deck, n):
    L = len(deck)
    new_deck = [0] * L
    current_idx = 0
    for card in deck:
        new_deck[current_idx] = card
        current_idx = (current_idx + n) % L
    return new_deck

def solve_part1_naive(data):
    instructions = parse_input(data)
    deck_size = 10007
    deck = list(range(deck_size))
    
    for line in instructions:
        if line == 'deal into new stack':
            deck = deal_into_new_stack(deck)
        elif line.startswith('cut '):
            n = int(line.split(' ')[-1])
            deck = cut_n(deck, n)
        elif line.startswith('deal with increment '):
            n = int(line.split(' ')[-1])
            deck = deal_with_increment_n(deck, n)
            
    return deck.index(2019)

def solve_part2(data):
    # Deck size: 119315717514047 (Prime?)
    # Shuffles: 101741582076661
    # What card is at position 2020?
    
    # We need to track the position transformation as a linear function modulo D.
    # pos -> a * pos + b (mod D)
    
    # Operations:
    # 1. Deal into new stack:
    #    pos -> D - 1 - pos
    #    pos -> -1 * pos + (D - 1)
    #    a = -1, b = D - 1
    
    # 2. Cut N:
    #    pos -> pos - N
    #    a = 1, b = -N
    
    # 3. Deal with increment N:
    #    pos -> pos * N
    #    a = N, b = 0
    
    # Composition of functions:
    # f(x) = ax + b
    # g(x) = cx + d
    # g(f(x)) = c(ax + b) + d = (ca)x + (cb + d)
    # New a' = c * a, New b' = c * b + d
    
    D = 119315717514047
    shuffles = 101741582076661
    
    instructions = parse_input(data)
    
    # Compose one round of shuffle
    a, b = 1, 0
    
    for line in instructions:
        if line == 'deal into new stack':
            # pos -> -pos - 1
            # a_new = -a
            # b_new = -b - 1
            a = (-a) % D
            b = (-b - 1) % D
        elif line.startswith('cut '):
            n = int(line.split(' ')[-1])
            # pos -> pos - n
            # a_new = a
            # b_new = b - n
            b = (b - n) % D
        elif line.startswith('deal with increment '):
            n = int(line.split(' ')[-1])
            # pos -> pos * n
            # a_new = a * n
            # b_new = b * n
            a = (a * n) % D
            b = (b * n) % D
            
    # Now we have f(x) = ax + b for one shuffle.
    # We want f^shuffles(x).
    # f^k(x) = a^k * x + b * (1 + a + ... + a^(k-1))
    # Sum of geometric series: (a^k - 1) / (a - 1)
    
    # Note: We want "what card is at position 2020".
    # This means we have the final position Y = 2020, and we want to find the initial position X.
    # In Part 1, we tracked X -> Y.
    # In Part 2, we want to invert the function: Y -> X.
    
    # The transformation we computed represents X -> Y (where does card X end up).
    # Y = A * X + B  (Final A, B after all shuffles)
    # We want X = (Y - B) * inv(A).
    
    # First, calculate coefficients A and B for k repetitions.
    
    inv_sq = pow(a - 1, D - 2, D) if a != 1 else None # modular inverse of a-1
    # Actually if a=1 (which is just shifting), sum is k.
    
    if a == 1:
        # f^k(x) = x + k * b
        final_a = 1
        final_b = (shuffles * b) % D
    else:
        # Geometric series sum: b * (a^k - 1) * inv(a-1)
        term = pow(a, shuffles, D)
        final_a = term
        final_b = (b * (term - 1) * pow(a - 1, D - 2, D)) % D
        
    # We have Y = final_a * X + final_b
    # We want X given Y = 2020.
    # X = (Y - final_b) * inv(final_a)
    
    Y = 2020
    inv_final_a = pow(final_a, D - 2, D)
    X = ((Y - final_b) * inv_final_a) % D
    
    return X

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    print("Part 1:", solve_part1_naive(data))
    print("Part 2:", solve_part2(data))

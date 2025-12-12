import os
import sys


def dance(programs, moves):
    """Perform one round of the dance."""
    progs = list(programs)
    n = len(progs)
    
    for move in moves:
        if move[0] == 's':
            x = int(move[1:])
            progs = progs[-x:] + progs[:-x]
        elif move[0] == 'x':
            a, b = map(int, move[1:].split('/'))
            progs[a], progs[b] = progs[b], progs[a]
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            ia, ib = progs.index(a), progs.index(b)
            progs[ia], progs[ib] = progs[ib], progs[ia]
    
    return progs


def part1(moves, n=16):
    """Perform dance once."""
    programs = [chr(ord('a') + i) for i in range(n)]
    programs = dance(programs, moves)
    return ''.join(programs)


def part2(moves, n=16, iterations=1_000_000_000):
    """Perform dance 1 billion times using cycle detection."""
    programs = [chr(ord('a') + i) for i in range(n)]
    initial = ''.join(programs)
    
    seen = {initial: 0}
    states = [initial]
    
    for i in range(1, iterations + 1):
        programs = dance(programs, moves)
        state = ''.join(programs)
        
        if state in seen:
            # Found cycle
            cycle_start = seen[state]
            cycle_len = i - cycle_start
            remaining = (iterations - cycle_start) % cycle_len
            return states[cycle_start + remaining]
        
        seen[state] = i
        states.append(state)
    
    return ''.join(programs)


def run_example():
    moves = ['s1', 'x3/4', 'pe/b']
    programs = list('abcde')
    programs = dance(programs, moves)
    assert ''.join(programs) == 'baedc'
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        moves = f.read().strip().split(',')
    
    print(f"Part 1: {part1(moves)}")
    print(f"Part 2: {part2(moves)}")

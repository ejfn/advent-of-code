import os
import sys
from collections import defaultdict, deque


def parse_instructions(text):
    """Parse program instructions."""
    return [line.split() for line in text.strip().split('\n') if line.strip()]


def get_value(regs, x):
    """Get value - either register or integer."""
    try:
        return int(x)
    except ValueError:
        return regs[x]


def part1(instructions):
    """Run until first rcv with non-zero value."""
    regs = defaultdict(int)
    last_sound = 0
    ip = 0
    
    while 0 <= ip < len(instructions):
        inst = instructions[ip]
        op = inst[0]
        
        if op == 'snd':
            last_sound = get_value(regs, inst[1])
        elif op == 'set':
            regs[inst[1]] = get_value(regs, inst[2])
        elif op == 'add':
            regs[inst[1]] += get_value(regs, inst[2])
        elif op == 'mul':
            regs[inst[1]] *= get_value(regs, inst[2])
        elif op == 'mod':
            regs[inst[1]] %= get_value(regs, inst[2])
        elif op == 'rcv':
            if get_value(regs, inst[1]) != 0:
                return last_sound
        elif op == 'jgz':
            if get_value(regs, inst[1]) > 0:
                ip += get_value(regs, inst[2])
                continue
        
        ip += 1
    
    return last_sound


def part2(instructions):
    """Two programs communicating via queues."""
    # Create two programs
    regs = [defaultdict(int), defaultdict(int)]
    regs[0]['p'] = 0
    regs[1]['p'] = 1
    
    queues = [deque(), deque()]  # queue[i] contains messages sent TO program i
    ip = [0, 0]
    waiting = [False, False]
    send_count = [0, 0]
    
    def get_val(pid, x):
        try:
            return int(x)
        except ValueError:
            return regs[pid][x]
    
    def step(pid):
        """Execute one instruction for program pid. Returns True if progress made."""
        nonlocal waiting
        
        if not (0 <= ip[pid] < len(instructions)):
            waiting[pid] = True
            return False
        
        inst = instructions[ip[pid]]
        op = inst[0]
        other = 1 - pid
        
        if op == 'snd':
            queues[other].append(get_val(pid, inst[1]))
            send_count[pid] += 1
        elif op == 'set':
            regs[pid][inst[1]] = get_val(pid, inst[2])
        elif op == 'add':
            regs[pid][inst[1]] += get_val(pid, inst[2])
        elif op == 'mul':
            regs[pid][inst[1]] *= get_val(pid, inst[2])
        elif op == 'mod':
            regs[pid][inst[1]] %= get_val(pid, inst[2])
        elif op == 'rcv':
            if queues[pid]:
                regs[pid][inst[1]] = queues[pid].popleft()
                waiting[pid] = False
            else:
                waiting[pid] = True
                return False  # Blocked
        elif op == 'jgz':
            if get_val(pid, inst[1]) > 0:
                ip[pid] += get_val(pid, inst[2])
                return True
        
        ip[pid] += 1
        return True
    
    # Run until deadlock
    while True:
        progress0 = step(0)
        progress1 = step(1)
        
        if not progress0 and not progress1:
            # Deadlock
            break
    
    return send_count[1]


def run_example():
    example = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
    instructions = parse_instructions(example)
    assert part1(instructions) == 4
    print("Part 1 example passed!")


if __name__ == "__main__":
    run_example()
    
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        instructions = parse_instructions(f.read())
    
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")

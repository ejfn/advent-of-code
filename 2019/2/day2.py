
import os
import sys

def run_intcode(memory):
    memory = list(memory) # copy so we don't mutate the original input list if reused
    pc = 0
    while True:
        opcode = memory[pc]
        if opcode == 99:
            break
        elif opcode == 1:
            p1, p2, p3 = memory[pc+1], memory[pc+2], memory[pc+3]
            memory[p3] = memory[p1] + memory[p2]
            pc += 4
        elif opcode == 2:
            p1, p2, p3 = memory[pc+1], memory[pc+2], memory[pc+3]
            memory[p3] = memory[p1] * memory[p2]
            pc += 4
        else:
            raise ValueError(f"Unknown opcode {opcode} at {pc}")
    return memory[0]

def part1(data):
    memory = [int(x) for x in data.split(',')]
    
    # Restore state as per instructions
    memory[1] = 12
    memory[2] = 2
    
    return run_intcode(memory)


def part2(data):
    initial_memory = [int(x) for x in data.split(',')]
    target = 19690720
    
    for noun in range(100):
        for verb in range(100):
            memory = list(initial_memory)
            memory[1] = noun
            memory[2] = verb
            
            try:
                result = run_intcode(memory)
            except Exception:
                # In case of invalid opcodes or index errors
                continue
            
            if result == target:
                return 100 * noun + verb
    return -1

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read().strip()

    # Part 1 logic is already verified
    
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")

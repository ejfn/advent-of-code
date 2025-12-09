
import os
import sys

def get_val(memory, pos, mode):
    if mode == 0: # Position
        return memory[memory[pos]]
    elif mode == 1: # Immediate
        return memory[pos]
    else:
        raise ValueError(f"Unknown mode {mode}")

def run_intcode(memory, inputs):
    memory = list(memory)
    pc = 0
    outputs = []
    input_idx = 0
    
    while True:
        instr = memory[pc]
        opcode = instr % 100
        # Modes: param1, param2, param3
        modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]
        
        if opcode == 99:
            break
            
        elif opcode == 1: # Add
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            dest = memory[pc + 3] # writes are always position mode (technically parameters, but effectively addresses)
            memory[dest] = v1 + v2
            pc += 4
            
        elif opcode == 2: # Mul
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            dest = memory[pc + 3]
            memory[dest] = v1 * v2
            pc += 4
            
        elif opcode == 3: # Input
            dest = memory[pc + 1]
            memory[dest] = inputs[input_idx]
            input_idx += 1
            pc += 2
            

        elif opcode == 4: # Output
            v1 = get_val(memory, pc + 1, modes[0])
            outputs.append(v1)
            pc += 2
            
        elif opcode == 5: # jump-if-true
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            if v1 != 0:
                pc = v2
            else:
                pc += 3
                
        elif opcode == 6: # jump-if-false
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            if v1 == 0:
                pc = v2
            else:
                pc += 3
        
        elif opcode == 7: # less-than
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            dest = memory[pc + 3]
            if v1 < v2:
                memory[dest] = 1
            else:
                memory[dest] = 0
            pc += 4
            
        elif opcode == 8: # equals
            v1 = get_val(memory, pc + 1, modes[0])
            v2 = get_val(memory, pc + 2, modes[1])
            dest = memory[pc + 3]
            if v1 == v2:
                memory[dest] = 1
            else:
                memory[dest] = 0
            pc += 4
            
        else:
            raise ValueError(f"Unknown opcode {opcode} at {pc}")
            
    return outputs

def part1(data):
    memory = [int(x) for x in data.split(',')]
    outputs = run_intcode(memory, inputs=[1])
    # Diagnostic code is the last output. Previous outputs should be 0.
    for out in outputs[:-1]:
        if out != 0:
            print(f"Test failed inside intcode computer: {out}")
    return outputs[-1]

def part2(data):
    memory = [int(x) for x in data.split(',')]
    outputs = run_intcode(memory, inputs=[5])
    return outputs[-1]

if __name__ == "__main__":
    input_path = os.path.join(sys.path[0], 'input.txt')
    with open(input_path) as f:
        data = f.read().strip()
    
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")

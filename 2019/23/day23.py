
import sys
import os
from collections import defaultdict, deque

class IntcodeComputer:
    def __init__(self, program, address):
        self.memory = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        self.pc = 0
        self.relative_base = 0
        self.inputs = deque([address])
        self.outputs = deque()
        self.halted = False
        self.address = address
        self.idle_count = 0 # To track idleness

    def get_addr(self, pos, mode):
        if mode == 0: return self.memory[pos]
        elif mode == 1: return pos
        elif mode == 2: return self.memory[pos] + self.relative_base
        else: raise ValueError(f"Unknown mode {mode}")

    def get_val(self, pos, mode):
        return self.memory[self.get_addr(pos, mode)]

    def set_val(self, pos, mode, val):
        self.memory[self.get_addr(pos, mode)] = val

    def add_input(self, val):
        self.inputs.append(val)
    
    def run_step(self):
        # Run until halt or I/O yield
        if self.halted: return False

        instr = self.memory[self.pc]
        opcode = instr % 100
        modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

        if opcode == 99:
            self.halted = True
            return False
        elif opcode == 1:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.set_val(self.pc + 3, modes[2], v1 + v2)
            self.pc += 4
        elif opcode == 2:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.set_val(self.pc + 3, modes[2], v1 * v2)
            self.pc += 4
        elif opcode == 3:
            if not self.inputs:
                # If no input, provide -1
                self.inputs.append(-1)
                self.idle_count += 1
            else:
                self.idle_count = 0
                
            self.set_val(self.pc + 1, modes[0], self.inputs.popleft())
            self.pc += 2
        elif opcode == 4:
            self.outputs.append(self.get_val(self.pc + 1, modes[0]))
            self.pc += 2
            self.idle_count = 0
            return True # Output generated
        elif opcode == 5:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.pc = v2 if v1 != 0 else self.pc + 3
        elif opcode == 6:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.pc = v2 if v1 == 0 else self.pc + 3
        elif opcode == 7:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.set_val(self.pc + 3, modes[2], 1 if v1 < v2 else 0)
            self.pc += 4
        elif opcode == 8:
            v1, v2 = self.get_val(self.pc + 1, modes[0]), self.get_val(self.pc + 2, modes[1])
            self.set_val(self.pc + 3, modes[2], 1 if v1 == v2 else 0)
            self.pc += 4
        elif opcode == 9:
            self.relative_base += self.get_val(self.pc + 1, modes[0])
            self.pc += 2
        else:
            raise ValueError(f"Unknown opcode {opcode}")
            
        return False

def solve_part1(program):
    computers = [IntcodeComputer(program, i) for i in range(50)]
    
    # Simulation loop
    # Round robin execution
    
    while True:
        for i, comp in enumerate(computers):
            # Run a few steps or until IO?
            # Instructions say "never block".
            # We can run one step at a time for all.
            
            # Since inputs are -1 if empty, we can just run until output or until input consumption?
            # IntcodeComputer.run_step runs one instruction.
            # We should probably run until output or a few instructions to make progress.
            # But let's verify if running one step implies slowness.
            # 50 computers...
            
            # Better strategy: Run each computer until it yields an output OR requests input when empty (-1).
            # My modified run_step handles -1 automatically.
            
            steps = 0
            while steps < 50: # execution slice
                has_out = comp.run_step()
                if has_out:
                    if len(comp.outputs) >= 3:
                        addr = comp.outputs.popleft()
                        x = comp.outputs.popleft()
                        y = comp.outputs.popleft()
                        
                        if addr == 255:
                            return y
                            
                        if 0 <= addr < 50:
                            computers[addr].add_input(x)
                            computers[addr].add_input(y)
                            
                        # Keep running this computer? Or yield?
                steps += 1

def solve_part2(program):
    # NAT (Not Always Transmitting) at 255.
    # When network idle, NAT sends packet to 0.
    
    computers = [IntcodeComputer(program, i) for i in range(50)]
    nat_packet = None
    last_nat_y_sent = None
    
    while True:
        idle_network = True
        
        for i, comp in enumerate(computers):
            # Run a slice
            steps = 0
            while steps < 50:
                has_out = comp.run_step()
                if has_out:
                    if len(comp.outputs) >= 3:
                        addr = comp.outputs.popleft()
                        x = comp.outputs.popleft()
                        y = comp.outputs.popleft()
                        
                        if addr == 255:
                            nat_packet = (x, y)
                        elif 0 <= addr < 50:
                            computers[addr].add_input(x)
                            computers[addr].add_input(y)
                steps += 1
                
            # Check idleness condition for this computer
            # If input queue is empty and last reading was -1?
            # My run_step doesn't strictly report "waiting for input".
            # But we can check if input queue is empty.
            if len(comp.inputs) > 0 or len(comp.outputs) > 0:
                idle_network = False
                
        # Also need to check if computers are actually effectively idle (reading -1s repeatedly)
        # We can loosely define idle if all input queues are empty?
        # But a computer might be processing a packet.
        # "Idle" means empty input queue and not producing output?
        # The problem says: "monitor all computers... if all computers have empty incoming packet queues and are continuously trying to receive packets without sending packets..."
        
        # We can assume if we run a full round and no packets flows (except -1 reads), it's idle.
        
        # Let's track activity in the round.
        
        if idle_network:
             # Need to confirm they are indeed reading -1. 
             # The loop runs instructions. If inputs are empty, it feeds -1.
             pass
             
        # Re-implement strict idle check:
        # 1. Input queue empty for all.
        # 2. No packets in flight (handled by immediate delivery in code above).
        
        # If idle_network is true here (all queues empty at end of round), 
        # is that enough? Maybe computers are busy processing?
        # "Continuously trying to receive packets"
        
        if idle_network:
             # Send NAT packet to 0
             if nat_packet:
                 x, y = nat_packet
                 if last_nat_y_sent == y:
                     return y
                 
                 last_nat_y_sent = y
                 computers[0].add_input(x)
                 computers[0].add_input(y)
                 nat_packet = None # Consumed? Or NAT stores last?
                 # "NAT remembers only the last packet it received."
                 # So we don't clear it, but we used it.
                 # Wait, if we receive a new packet 255, it overwrites.
                 
                 # But we just sent it.
                 # Loop continues.

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    print("Part 1:", solve_part1(list(program)))
    print("Part 2:", solve_part2(list(program)))

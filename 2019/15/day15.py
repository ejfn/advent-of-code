
import sys
import os
from collections import defaultdict, deque
import copy

class IntcodeComputer:
    def __init__(self, program):
        self.memory = defaultdict(int)
        for i, val in enumerate(program):
            self.memory[i] = val
        self.pc = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = deque()
        self.halted = False
        self.waiting_for_input = False

    def copy(self):
        new_comp = IntcodeComputer([])
        new_comp.memory = self.memory.copy()
        new_comp.pc = self.pc
        new_comp.relative_base = self.relative_base
        new_comp.inputs = copy.copy(self.inputs)
        new_comp.outputs = copy.copy(self.outputs)
        new_comp.halted = self.halted
        new_comp.waiting_for_input = self.waiting_for_input
        return new_comp

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
        self.waiting_for_input = False

    def has_output(self):
        return len(self.outputs) > 0
    
    def get_output(self):
        return self.outputs.popleft() if self.outputs else None

    def run(self):
        while True:
            instr = self.memory[self.pc]
            opcode = instr % 100
            modes = [(instr // 100) % 10, (instr // 1000) % 10, (instr // 10000) % 10]

            if opcode == 99:
                self.halted = True
                return
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
                    self.waiting_for_input = True
                    return # Suspends execution waiting for input
                self.set_val(self.pc + 1, modes[0], self.inputs.popleft())
                self.pc += 2
            elif opcode == 4:
                self.outputs.append(self.get_val(self.pc + 1, modes[0]))
                self.pc += 2
                return # Yield on output
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

def bfs_explore(program):
    # Directions: 1=N, 2=S, 3=W, 4=E
    # 0=Wall, 1=Moved, 2=Oxygen
    dx = {1: 0, 2: 0, 3: -1, 4: 1}
    dy = {1: -1, 2: 1, 3: 0, 4: 0}
    back = {1: 2, 2: 1, 3: 4, 4: 3}
    
    # We can't easily clone the computer state every step if it's large, but Intcode memory can be large.
    # However, since we need to explore a maze, we can use a "re-run to state" approach or just backtracking DFS 
    # to build the map, then BFS on the map.
    # Given the Intcode computer size, cloning for BFS queue might be heavy but let's see. 
    # State-based BFS is safest for shortest path if state fits in memory.
    
    # Actually, "fewest number of movement commands" implies shortest path.
    # Since we can move freely back and forth (except walls), we can map the whole area first with DFS/BFS
    # and then find the shortest path in the grid.
    
    # Let's map the area using DFS with backtracking.
    
    computer = IntcodeComputer(program)
    grid = {} # (x,y) -> status
    grid[(0,0)] = 1 # Start is open
    
    oxygen_pos = None
    
    # DFS stack: (x, y, path_from_start)
    # Actually, we need to move the robot.
    # Recursive DFS is easier.
    
    def dfs(x, y, comp):
        nonlocal oxygen_pos
        
        for move in [1, 2, 3, 4]:
            nx, ny = x + dx[move], y + dy[move]
            
            if (nx, ny) not in grid:
                # Try to move
                comp.add_input(move)
                comp.run()
                status = comp.get_output()
                
                grid[(nx, ny)] = status
                
                if status == 0:
                    # Wall, didn't move
                    pass
                elif status == 1 or status == 2:
                    if status == 2:
                        oxygen_pos = (nx, ny)
                    
                    # Successfully moved, continue exploration from there
                    dfs(nx, ny, comp)
                    
                    # Backtrack
                    comp.add_input(back[move])
                    comp.run()
                    comp.get_output() # Ignore backtrack output (should be 1)
                    
    dfs(0, 0, computer)
    
    return grid, oxygen_pos

def solve_part1(program):
    grid, oxygen_pos = bfs_explore(program)
    
    # Now BFS on the known grid to find shortest path from (0,0) to oxygen_pos
    queue = deque([(0, 0, 0)])
    visited = set([(0, 0)])
    
    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == oxygen_pos:
            return dist, grid, oxygen_pos
            
        for move in [1, 2, 3, 4]:
            dx_map = {1: 0, 2: 0, 3: -1, 4: 1}
            dy_map = {1: -1, 2: 1, 3: 0, 4: 0}
            
            nx, ny = x + dx_map[move], y + dy_map[move]
            
            if (nx, ny) in grid and grid[(nx, ny)] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))
                
    return -1, grid, oxygen_pos

def solve_part2(grid, start_pos):
    # BFS to find furthest point from oxygen system (fill time)
    queue = deque([(start_pos[0], start_pos[1], 0)])
    visited = set([start_pos])
    max_minutes = 0
    
    while queue:
        x, y, minutes = queue.popleft()
        max_minutes = max(max_minutes, minutes)
        
        for move in [1, 2, 3, 4]:
            dx_map = {1: 0, 2: 0, 3: -1, 4: 1}
            dy_map = {1: -1, 2: 1, 3: 0, 4: 0}
            
            nx, ny = x + dx_map[move], y + dy_map[move]
            
            if (nx, ny) in grid and grid[(nx, ny)] != 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, minutes + 1))
                
    return max_minutes

if __name__ == "__main__":
    infile = os.path.join(sys.path[0], 'input.txt')
    with open(infile, 'r') as f:
        data = f.read().strip()
    
    program = [int(x) for x in data.split(',')]
    
    dist, grid, oxygen_pos = solve_part1(program)
    print("Part 1:", dist)
    
    # Part 2 is often about filling the area with oxygen
    print("Part 2:", solve_part2(grid, oxygen_pos))

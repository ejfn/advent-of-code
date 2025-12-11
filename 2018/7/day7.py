import sys
import os
import re
import heapq
from collections import defaultdict, deque

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    all_nodes = set()
    
    pattern = re.compile(r"Step (\w) must be finished before step (\w) can begin.")
    
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            src, dst = match.groups()
            adj[src].append(dst)
            in_degree[dst] += 1
            all_nodes.add(src)
            all_nodes.add(dst)
            
    return adj, in_degree, all_nodes

def solve_part1(adj, in_degree, all_nodes):
    # Make a copy of in_degree to not mutate for part 2 if needed
    current_in_degree = in_degree.copy()
    
    # Find all nodes with 0 in-degree
    queue = []
    for node in all_nodes:
        if current_in_degree[node] == 0:
            heapq.heappush(queue, node)
            
    result = []
    while queue:
        node = heapq.heappop(queue)
        result.append(node)
        
        if node in adj:
            for neighbor in adj[node]:
                current_in_degree[neighbor] -= 1
                if current_in_degree[neighbor] == 0:
                    heapq.heappush(queue, neighbor)
                    
    return "".join(result)

def solve_part2(adj, in_degree, all_nodes, num_workers=5, base_time=60):
    current_in_degree = in_degree.copy()
    
    # Priority queue of available tasks
    available = []
    for node in all_nodes:
        if current_in_degree[node] == 0:
            heapq.heappush(available, node)
            
    # Workers: list of (finish_time, task_node)
    # Using None to represent no task
    workers = [(0, None)] * num_workers
    
    current_time = 0
    completed = []
    
    while len(completed) < len(all_nodes):
        # 1. Check for completed tasks
        # Sort workers to process earliest completion first? 
        # Actually, we should advance time to the earliest finish time among busy workers,
        # OR just iterate second by second?
        # Event based is better.
        
        # Find earliest finish time of a BUSY worker
        busy_workers = [w for w in workers if w[1] is not None]
        if not busy_workers:
            # All idle, pick up tasks immediately at current_time
            pass
        else:
            # Sort busy workers by finish time
            busy_workers.sort(key=lambda x: x[0])
            next_event_time = busy_workers[0][0]
            
            # If we have available tasks and free workers, we might start something NOW
            # before jumping to next event.
            # But if all workers are busy, jump.
            # If some workers are free, we can assign.
            
            # Simplest correct logic:
            # Standard loop:
            # - Check available tasks can be assigned to free workers?
            # - If yes, assign.
            # - If no (no tasks OR no workers), jump to next completion.
            pass

        # Let's refine the loop
        # We need to process events in order.
        
        # Check if any worker finished at or before current_time
        # (This handles the case where multiple finish at same time)
        progress_made = False
        
        for i in range(num_workers):
            finish_time, node = workers[i]
            if node is not None and finish_time <= current_time:
                # Task finished
                completed.append(node)
                workers[i] = (current_time, None) # Free worker
                
                # Unlock neighbors
                if node in adj:
                    for neighbor in adj[node]:
                        current_in_degree[neighbor] -= 1
                        if current_in_degree[neighbor] == 0:
                            heapq.heappush(available, neighbor)
                progress_made = True
                
        # Assign available tasks to free workers
        # Free workers are those with w[1] is None
        free_indices = [i for i, w in enumerate(workers) if w[1] is None]
        
        while free_indices and available:
            idx = free_indices.pop(0)
            node = heapq.heappop(available)
            duration = base_time + (ord(node) - ord('A') + 1)
            finish_time = current_time + duration
            workers[idx] = (finish_time, node)
            progress_made = True
        
        # Determine next time step
        # If any worker is busy, next event is min(finish_time of busy workers)
        # If all workers free and no tasks available -> Done (handled by while condition)
        
        busy_finish_times = [w[0] for w in workers if w[1] is not None]
        if not busy_finish_times:
             if len(completed) < len(all_nodes):
                 # Should not happen unless graph disconnected or logic bug
                 # If we are here, we have no busy workers, but tasks remain.
                 # Means we have available tasks (just assigned) or we are stuck.
                 pass
             else:
                 break # Done
        else:
            # Jump to next event
            min_finish = min(busy_finish_times)
            current_time = max(current_time, min_finish)
            
    return current_time

def part1():
    adj, in_degree, all_nodes = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part1(adj, in_degree, all_nodes)
    print(f'Part 1: {result}')
    return result

def part2():
    adj, in_degree, all_nodes = parse_input(os.path.join(sys.path[0], 'input.txt'))
    result = solve_part2(adj, in_degree, all_nodes, num_workers=5, base_time=60)
    print(f'Part 2: {result}')
    return result

def run_example():
    print("Running Example...")
    # Manually constructing example graph from description
    # C -> A, C -> F, A -> B, A -> D, B -> E, D -> E, F -> E
    adj = defaultdict(list)
    adj['C'] = ['A', 'F']
    adj['A'] = ['B', 'D']
    adj['B'] = ['E']
    adj['D'] = ['E']
    adj['F'] = ['E']
    
    in_degree = defaultdict(int)
    in_degree['A'] = 1
    in_degree['F'] = 1
    in_degree['B'] = 1
    in_degree['D'] = 1
    in_degree['E'] = 3
    in_degree['C'] = 0 # Explicitly 0
    
    all_nodes = {'A', 'B', 'C', 'D', 'E', 'F'}
    
    result = solve_part1(adj, in_degree, all_nodes)
    print(f"Example Part 1 Result: {result}")
    assert result == "CABDFE"
    
    # Part 2 Example
    p2_result = solve_part2(adj, in_degree, all_nodes, num_workers=2, base_time=0)
    print(f"Example Part 2 Result: {p2_result}")
    assert p2_result == 15

if __name__ == '__main__':
    run_example()
    part1()
    part2()

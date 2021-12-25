import itertools
import time
from collections import defaultdict
from heapq import heappop, heappush


hallway = [0, 1, 3, 5, 7, 9, 10]
rooms = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}
move_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
room_capacity = 2


class State:
    def __init__(self, init) -> None:
        self.parent = None
        self.state = defaultdict(lambda: [])
        for i in init:
            self.state[i] = init[i].copy()

    def __key__(self):
        return ';'.join([str(i) + '=' + ''.join(self.state[i]) for i in range(11) if len(self.state[i]) > 0])

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__key__() == other.__key__()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, State):
            return self.__key__() < other.__key__()
        return NotImplemented

    def print_hallway(self):
        h = ''.join('.' if i in rooms else self.state[i][-1]
                    if len(self.state[i]) > 0 else '.' for i in range(11))
        print('#' + h + '#')

    def print_room(self, i):
        r = '#'.join(self.state[r][i] if len(
            self.state[r]) > i else '.' for r in rooms)
        if i == room_capacity - 1:
            print('###' + r + '###')
        else:
            print('  #' + r + '#  ')

    def print(self):
        print('#############')
        self.print_hallway()
        for i in range(room_capacity, 0, -1):
            self.print_room(i - 1)
        print('  #########  ')

    def is_available(self, a: str, pos: int):
        if pos in rooms:
            return a == rooms[pos] and len(self.state[pos]) < room_capacity and all([a == x for x in self.state[pos]])
        else:
            return len(self.state[pos]) == 0

    def not_blocked(self, start, end) -> bool:
        s = min(start, end)
        d = max(start, end)
        for i in range(s+1, d):
            if i in rooms:
                continue
            elif len(self.state[i]) > 0:
                return False
        return True

    def find_next_moves(self):
        for s, e in itertools.product(range(11), repeat=2):
            if len(self.state[s]) == 0 or s == e or (s in hallway and e in hallway):
                continue
            items = self.state[s]
            a = items[-1]
            if self.is_available(a, e) and self.not_blocked(s, e):
                cp = State(self.state)
                q = cp.state[s].pop()
                cp.state[e].append(q)
                yield (cp, cp.cost(a, e, s))

    def cost(self, amph, start, end):
        steps = abs(start - end)
        if start in rooms:
            steps += room_capacity - len(self.state[start]) + 1
        if end in rooms:
            steps += room_capacity - len(self.state[end])
        return steps * move_cost[amph]


def dijkstra(start: State, end: State):
    solved, costs, hpq = set(), dict(), []
    costs[start] = 0
    heappush(hpq, (0, start))
    while hpq:
        cost, k = heappop(hpq)
        if k in solved:
            continue
        solved.add(k)
        if k == end:
            end.parent = k.parent
            return cost
        for adj, c in k.find_next_moves():
            if adj in solved:
                continue
            acc_cost = cost + c
            if adj not in costs or acc_cost < costs[adj]:
                adj.parent = k
                costs[adj] = acc_cost
                heappush(hpq, (acc_cost, adj))
    return float('inf')


def print_path(target: State, rewrite_lines, wait):
    path = [target]
    while path[0].parent is not None:
        path.insert(0, path[0].parent)
    print('\n' * rewrite_lines, end='')
    for p in path:
        print('\033[F' * (rewrite_lines + 1))
        p.print()
        time.sleep(wait)


def part1():
    initial = State({
        2: ['B', 'D'],
        4: ['C', 'D'],
        6: ['A', 'B'],
        8: ['C', 'A']
    })
    target = State({
        2: ['A', 'A'],
        4: ['B', 'B'],
        6: ['C', 'C'],
        8: ['D', 'D']
    })
    print(dijkstra(initial, target))
    print_path(target, 5, 0.5)


def part2():
    global room_capacity
    room_capacity = 4
    initial = State({
        2: ['B', 'D', 'D', 'D'],
        4: ['C', 'B', 'C', 'D'],
        6: ['A', 'A', 'B', 'B'],
        8: ['C', 'C', 'A', 'A']
    })
    target = State({
        2: ['A', 'A', 'A', 'A'],
        4: ['B', 'B', 'B', 'B'],
        6: ['C', 'C', 'C', 'C'],
        8: ['D', 'D', 'D', 'D']
    })
    print(dijkstra(initial, target))
    print_path(target, 7, 0.5)


part1()  # 16244
part2()  # 43226

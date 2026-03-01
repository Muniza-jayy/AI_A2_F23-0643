# search.py
import heapq
from typing import Callable, Dict, List, Set, Tuple
from model import GridWorld, Cell

def reconstruct_path(parent: Dict[Cell, Cell], start: Cell, goal: Cell) -> List[Cell]:
    if goal != start and goal not in parent:
        return []
    cur = goal
    path = [cur]
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path

def gbfs(world: GridWorld, h: Callable[[Cell, Cell], float]) -> Tuple[List[Cell], List[Cell], int]:
    start, goal = world.start, world.goal

    pq = []
    tie = 0
    heapq.heappush(pq, (h(start, goal), tie, start))

    parent: Dict[Cell, Cell] = {}
    visited: Set[Cell] = set()
    expanded_order: List[Cell] = []

    while pq:
        _, _, cur = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)
        expanded_order.append(cur)

        if cur == goal:
            return reconstruct_path(parent, start, goal), expanded_order, len(expanded_order)

        for nb in world.neighbors8(cur):
            if nb not in visited:
                if nb not in parent:
                    parent[nb] = cur
                tie += 1
                heapq.heappush(pq, (h(nb, goal), tie, nb))

    return [], expanded_order, len(expanded_order)

def astar(world: GridWorld, h: Callable[[Cell, Cell], float]) -> Tuple[List[Cell], List[Cell], int]:
    start, goal = world.start, world.goal

    pq = []
    tie = 0

    g: Dict[Cell, int] = {start: 0}
    parent: Dict[Cell, Cell] = {}
    visited: Set[Cell] = set()
    expanded_order: List[Cell] = []

    heapq.heappush(pq, (g[start] + h(start, goal), tie, start))

    while pq:
        _, _, cur = heapq.heappop(pq)
        if cur in visited:
            continue

        visited.add(cur)
        expanded_order.append(cur)

        if cur == goal:
            return reconstruct_path(parent, start, goal), expanded_order, len(expanded_order)

        for nb in world.neighbors8(cur):
            new_g = g[cur] + 1  # cost per move = 1
            if nb not in g or new_g < g[nb]:
                g[nb] = new_g
                parent[nb] = cur
                tie += 1
                heapq.heappush(pq, (new_g + h(nb, goal), tie, nb))

    return [], expanded_order, len(expanded_order)
# search.py
import heapq
from typing import Callable, Dict, List, Set, Tuple
from model import GridWorld

Cell = Tuple[int, int]
Heuristic = Callable[[Cell, Cell], float]


def reconstruct_path(parent: Dict[Cell, Cell], start: Cell, goal: Cell) -> List[Cell]:
    if start == goal:
        return [start]
    if goal not in parent:
        return []
    cur = goal
    path = [cur]
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def gbfs(world: GridWorld, h: Heuristic):
    """
    Returns: (path, expanded_order, expanded_count, frontier_set)
    """
    start, goal = world.start, world.goal

    pq = []
    tie = 0
    heapq.heappush(pq, (h(start, goal), tie, start))

    parent: Dict[Cell, Cell] = {}
    visited: Set[Cell] = set()
    expanded_order: List[Cell] = []
    frontier_set: Set[Cell] = {start}

    while pq:
        _, _, cur = heapq.heappop(pq)
        frontier_set.discard(cur)

        if cur in visited:
            continue

        visited.add(cur)
        expanded_order.append(cur)

        if cur == goal:
            path = reconstruct_path(parent, start, goal)
            return path, expanded_order, len(expanded_order), frontier_set

        for nb in world.neighbors8(cur):
            if nb in visited:
                continue
            if nb not in parent:
                parent[nb] = cur
            tie += 1
            heapq.heappush(pq, (h(nb, goal), tie, nb))
            frontier_set.add(nb)

    return [], expanded_order, len(expanded_order), frontier_set


def astar(world: GridWorld, h: Heuristic):
    """
    Returns: (path, expanded_order, expanded_count, frontier_set)
    """
    start, goal = world.start, world.goal

    pq = []
    tie = 0

    g_cost: Dict[Cell, int] = {start: 0}
    parent: Dict[Cell, Cell] = {}
    visited: Set[Cell] = set()
    expanded_order: List[Cell] = []
    frontier_set: Set[Cell] = {start}

    heapq.heappush(pq, (h(start, goal), tie, start))

    while pq:
        _, _, cur = heapq.heappop(pq)
        frontier_set.discard(cur)

        if cur in visited:
            continue

        visited.add(cur)
        expanded_order.append(cur)

        if cur == goal:
            path = reconstruct_path(parent, start, goal)
            return path, expanded_order, len(expanded_order), frontier_set

        for nb in world.neighbors8(cur):
            new_g = g_cost[cur] + 1
            if nb not in g_cost or new_g < g_cost[nb]:
                g_cost[nb] = new_g
                parent[nb] = cur
                tie += 1
                f = new_g + h(nb, goal)
                heapq.heappush(pq, (f, tie, nb))
                if nb not in visited:
                    frontier_set.add(nb)

    return [], expanded_order, len(expanded_order), frontier_set
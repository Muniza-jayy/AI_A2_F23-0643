# model.py
from dataclasses import dataclass
from typing import List, Tuple, Set

Cell = Tuple[int, int]

@dataclass
class GridWorld:
    rows: int
    cols: int
    start: Cell
    goal: Cell
    walls: Set[Cell]

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, cell: Cell) -> bool:
        return cell not in self.walls

    def neighbors8(self, cell: Cell) -> List[Cell]:
        r, c = cell
        moves = [
            (-1, 0),   # Up
            (-1, 1),   # Top-Right
            (0, 1),    # Right
            (1, 1),    # Bottom-Right
            (1, 0),    # Bottom
            (1, -1),   # Bottom-Left
            (0, -1),   # Left
            (-1, -1),  # Top-Left
        ]
        out = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if self.in_bounds(nr, nc) and self.passable(nxt):
                out.append(nxt)
        return out
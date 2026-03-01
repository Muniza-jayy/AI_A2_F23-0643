# heuristics.py
from typing import Tuple
import math

Cell = Tuple[int, int]

def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a: Cell, b: Cell) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

HEURISTICS = {
    "Manhattan": manhattan,
    "Euclidean": euclidean,
}
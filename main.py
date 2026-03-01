# main.py
import tkinter as tk
from tkinter import ttk
import random
import time

from model import GridWorld
from heuristics import HEURISTICS
from search import gbfs, astar

CELL_SIZE = 35

ALGOS = {
    "Greedy Best-First (f=h)": gbfs,
    "A* (f=g+h)": astar,
}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GOOD PERFORMANCE TIME APP")

        # ---- Left panel ----
        panel = ttk.Frame(root)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(panel, text="Rows").pack(anchor="w")
        self.rows_var = tk.IntVar(value=10)
        ttk.Entry(panel, textvariable=self.rows_var, width=6).pack(anchor="w")

        ttk.Label(panel, text="Cols").pack(anchor="w", pady=(6,0))
        self.cols_var = tk.IntVar(value=14)
        ttk.Entry(panel, textvariable=self.cols_var, width=6).pack(anchor="w")

        ttk.Label(panel, text="Obstacle Density (0-1)").pack(anchor="w", pady=(10,0))
        self.density_var = tk.DoubleVar(value=0.3)
        ttk.Entry(panel, textvariable=self.density_var, width=6).pack(anchor="w")

        ttk.Label(panel, text="Algorithm").pack(anchor="w", pady=(12,0))
        self.algo_var = tk.StringVar(value=list(ALGOS.keys())[1])
        ttk.Combobox(panel, textvariable=self.algo_var, values=list(ALGOS.keys()), state="readonly").pack(anchor="w", fill=tk.X)

        ttk.Label(panel, text="Heuristic").pack(anchor="w", pady=(12,0))
        self.h_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(panel, textvariable=self.h_var, values=list(HEURISTICS.keys()), state="readonly").pack(anchor="w", fill=tk.X)

        ttk.Button(panel, text="Create Grid", command=self.create_grid).pack(fill=tk.X, pady=(12,4))
        ttk.Button(panel, text="Random Map", command=self.random_map).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Run", command=self.run).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Clear Search (keep walls)", command=self.clear_search).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Exit", command=root.destroy).pack(fill=tk.X, pady=(20,0))

        ttk.Label(panel, text="Metrics", font=("Arial", 11, "bold")).pack(anchor="w", pady=(18,6))
        self.metrics_var = tk.StringVar(value="Nodes: 0\nCost: 0\nTime: 0 ms")
        ttk.Label(panel, textvariable=self.metrics_var).pack(anchor="w")

        # ---- Canvas ----
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

        # world state
        self.world = None
        self.grid_data = []
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None
        self.walls = set()

        # search visualization sets
        self.visited = set()
        self.path = []

        self.create_grid()

    # ---------- Grid setup ----------
    def create_grid(self):
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()

        self.grid_data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.start = (self.rows - 2, self.cols - 3)
        self.goal  = (self.rows - 3, 1)

        self.walls = set()
        self.clear_search()
        self.draw()

    def random_map(self):
        density = self.density_var.get()
        self.walls.clear()

        for r in range(self.rows):
            for c in range(self.cols):
                cell = (r, c)
                if cell in (self.start, self.goal):
                    continue
                if random.random() < density:
                    self.walls.add(cell)

        self.clear_search()
        self.draw()

    def on_click(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            cell = (r, c)
            if cell in (self.start, self.goal):
                return
            # toggle wall
            if cell in self.walls:
                self.walls.remove(cell)
            else:
                self.walls.add(cell)

            self.clear_search()
            self.draw()

    # ---------- Visualization ----------
    def clear_search(self):
        self.visited = set()
        self.path = []
        self.metrics_var.set("Nodes: 0\nCost: 0\nTime: 0 ms")

    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                cell = (r, c)

                color = "white"
                if cell in self.walls:
                    color = "black"
                elif cell in self.visited:
                    color = "#9db7ff"     # visited (blue-ish)
                elif cell in self.path:
                    color = "lime"        # final path

                if cell == self.start:
                    color = "green"
                if cell == self.goal:
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                if cell == self.start:
                    self.canvas.create_text(x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                                            text="S", fill="white", font=("Arial", 12, "bold"))
                if cell == self.goal:
                    self.canvas.create_text(x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                                            text="G", fill="white", font=("Arial", 12, "bold"))

        self.root.update_idletasks()

    # ---------- Run Search ----------
    def run(self):
        # build world object
        self.world = GridWorld(self.rows, self.cols, self.start, self.goal, set(self.walls))

        algo_fn = ALGOS[self.algo_var.get()]
        h_fn = HEURISTICS[self.h_var.get()]

        # run algorithm (static)
        t0 = time.perf_counter()
        path, expanded_order, expanded_count = algo_fn(self.world, h_fn)
        ms = (time.perf_counter() - t0) * 1000.0

        # animate expansions
        self.visited = set()
        self.path = []
        for node in expanded_order:
            self.visited.add(node)
            self.draw()
            self.root.update()
            self.root.after(35)  # animation speed

        # show final path
        self.path = path
        self.draw()

        cost = max(0, len(path) - 1)
        if not path:
            self.metrics_var.set(f"Nodes: {expanded_count}\nCost: 0\nTime: {ms:.1f} ms\nNo path!")
        else:
            self.metrics_var.set(f"Nodes: {expanded_count}\nCost: {cost}\nTime: {ms:.1f} ms")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
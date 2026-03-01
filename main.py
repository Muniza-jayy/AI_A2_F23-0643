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

        ttk.Label(panel, text="Cols").pack(anchor="w", pady=(6, 0))
        self.cols_var = tk.IntVar(value=14)
        ttk.Entry(panel, textvariable=self.cols_var, width=6).pack(anchor="w")

        ttk.Label(panel, text="Obstacle Density (0-1)").pack(anchor="w", pady=(10, 0))
        self.density_var = tk.DoubleVar(value=0.30)
        ttk.Entry(panel, textvariable=self.density_var, width=6).pack(anchor="w")

        ttk.Label(panel, text="Algorithm").pack(anchor="w", pady=(12, 0))
        self.algo_var = tk.StringVar(value=list(ALGOS.keys())[1])
        ttk.Combobox(
            panel,
            textvariable=self.algo_var,
            values=list(ALGOS.keys()),
            state="readonly",
        ).pack(anchor="w", fill=tk.X)

        ttk.Label(panel, text="Heuristic").pack(anchor="w", pady=(12, 0))
        self.h_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(
            panel,
            textvariable=self.h_var,
            values=list(HEURISTICS.keys()),
            state="readonly",
        ).pack(anchor="w", fill=tk.X)

        # Dynamic controls
        ttk.Label(panel, text="Dynamic Mode").pack(anchor="w", pady=(12, 0))
        self.dynamic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(panel, text="Enable", variable=self.dynamic_var).pack(anchor="w")

        ttk.Label(panel, text="Spawn Probability (0-1)").pack(anchor="w", pady=(6, 0))
        self.spawn_p_var = tk.DoubleVar(value=0.07)
        ttk.Entry(panel, textvariable=self.spawn_p_var, width=6).pack(anchor="w")

        ttk.Button(panel, text="Create Grid", command=self.create_grid).pack(fill=tk.X, pady=(12, 4))
        ttk.Button(panel, text="Random Map", command=self.random_map).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Run", command=self.run).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Clear Search (keep walls)", command=self.clear_search).pack(fill=tk.X, pady=4)
        ttk.Button(panel, text="Exit", command=root.destroy).pack(fill=tk.X, pady=(20, 0))

        ttk.Label(panel, text="Metrics", font=("Arial", 11, "bold")).pack(anchor="w", pady=(18, 6))
        self.metrics_var = tk.StringVar(value="Nodes: 0\nCost: 0\nTime: 0 ms\nReplans: 0")
        ttk.Label(panel, textvariable=self.metrics_var).pack(anchor="w")

        # ---- Canvas ----
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

        # World state
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None
        self.walls = set()

        # Search visualization sets
        self.visited = set()
        self.frontier = set()   # ✅ NEW
        self.path = []
        self.agent_pos = None

        self.create_grid()

    # ---------- Grid setup ----------
    def create_grid(self):
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()

        self.start = (self.rows - 2, self.cols - 3)
        self.goal = (self.rows - 3, 1)
        self.agent_pos = self.start

        self.walls = set()
        self.clear_search()
        self.draw()

    def random_map(self):
        density = float(self.density_var.get())
        self.walls.clear()

        for r in range(self.rows):
            for c in range(self.cols):
                cell = (r, c)
                if cell in (self.start, self.goal):
                    continue
                if random.random() < density:
                    self.walls.add(cell)

        self.agent_pos = self.start
        self.clear_search()
        self.draw()

    def on_click(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            cell = (r, c)
            if cell in (self.start, self.goal):
                return
            if cell in self.walls:
                self.walls.remove(cell)
            else:
                self.walls.add(cell)

            self.clear_search()
            self.draw()

    # ---------- Visualization ----------
    def clear_search(self):
        self.visited = set()
        self.frontier = set()   # ✅ NEW
        self.path = []
        if self.agent_pos is None:
            self.agent_pos = self.start
        self.metrics_var.set("Nodes: 0\nCost: 0\nTime: 0 ms\nReplans: 0")

    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                cell = (r, c)

                # Base color
                if cell in self.walls:
                    color = "black"
                else:
                    color = "white"

                # Overlays (frontier first, then visited, then path)
                if cell in self.frontier and cell not in (self.start, self.goal):
                    color = "yellow"
                if cell in self.visited and cell not in (self.start, self.goal):
                    color = "#9db7ff"  # visited
                if cell in self.path and cell not in (self.start, self.goal):
                    color = "lime"  # path

                # Start/Goal
                if cell == self.start:
                    color = "green"
                if cell == self.goal:
                    color = "red"

                # Agent (top overlay)
                if cell == self.agent_pos and cell not in (self.start, self.goal):
                    color = "orange"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                # Labels always visible
                if cell == self.start:
                    self.canvas.create_text(
                        x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                        text="S", fill="white", font=("Arial", 12, "bold")
                    )
                if cell == self.goal:
                    self.canvas.create_text(
                        x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                        text="G", fill="white", font=("Arial", 12, "bold")
                    )

        self.root.update_idletasks()

    # ---------- Helpers ----------
    def spawn_dynamic_wall(self):
        """Spawn a wall in a random empty location (not start/goal/agent). Returns spawned cell or None."""
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in self.walls
            and (r, c) not in (self.start, self.goal, self.agent_pos)
        ]
        if not candidates:
            return None
        new_wall = random.choice(candidates)
        self.walls.add(new_wall)
        return new_wall

    # ---------- Run Search with Dynamic Replanning ----------
    def run(self):
        # reset only visited/frontier/path but keep walls
        self.visited = set()
        self.frontier = set()   # ✅ NEW
        self.path = []
        self.agent_pos = self.start

        algo_fn = ALGOS[self.algo_var.get()]
        h_fn = HEURISTICS[self.h_var.get()]

        total_expanded = 0
        total_time_ms = 0.0
        replans = 0

        current_pos = self.agent_pos

        while current_pos != self.goal:
            world = GridWorld(self.rows, self.cols, current_pos, self.goal, set(self.walls))

            t0 = time.perf_counter()
            path, expanded_order, expanded_count, frontier = algo_fn(world, h_fn)
            elapsed = (time.perf_counter() - t0) * 1000.0

            total_expanded += expanded_count
            total_time_ms += elapsed

            if not path:
                self.metrics_var.set(
                    f"Nodes: {total_expanded}\nCost: 0\nTime: {total_time_ms:.1f} ms\nReplans: {replans}\nBlocked!"
                )
                self.draw()
                return

            # store frontier for drawing
            self.frontier = set(frontier)

            # Animate expansions for THIS plan
            for node in expanded_order:
                self.visited.add(node)
                self.draw()
                self.root.update()
                self.root.after(20)

            # Move along planned path (one step at a time)
            remaining = path[:]  # includes current_pos
            while len(remaining) > 1:
                nxt = remaining[1]
                self.agent_pos = nxt
                current_pos = nxt

                # show remaining path from current position
                self.path = remaining
                self.draw()
                self.root.update()
                self.root.after(120)

                # Dynamic obstacle
                if self.dynamic_var.get():
                    p = float(self.spawn_p_var.get())
                    if random.random() < p:
                        spawned = self.spawn_dynamic_wall()

                        # If it blocks remaining path => replan
                        if spawned and spawned in set(remaining[1:]):
                            replans += 1
                            break

                remaining = remaining[1:]

                if current_pos == self.goal:
                    break

            cost = max(0, len(path) - 1)
            self.metrics_var.set(
                f"Nodes: {total_expanded}\nCost: {cost}\nTime: {total_time_ms:.1f} ms\nReplans: {replans}"
            )

        final_cost = max(0, len(self.path) - 1)
        self.metrics_var.set(
            f"Nodes: {total_expanded}\nCost: {final_cost}\nTime: {total_time_ms:.1f} ms\nReplans: {replans}\nReached Goal ✅"
        )
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
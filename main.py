import tkinter as tk
from tkinter import ttk
import random

CELL_SIZE = 35

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GOOD PERFORMANCE TIME APP")

        # ---- Controls Panel ----
        control = ttk.Frame(root)
        control.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(control, text="Rows").pack(anchor="w")
        self.rows_var = tk.IntVar(value=10)
        ttk.Entry(control, textvariable=self.rows_var, width=5).pack(anchor="w")

        ttk.Label(control, text="Cols").pack(anchor="w")
        self.cols_var = tk.IntVar(value=14)
        ttk.Entry(control, textvariable=self.cols_var, width=5).pack(anchor="w")

        ttk.Label(control, text="Obstacle Density (0-1)").pack(anchor="w", pady=(10,0))
        self.density_var = tk.DoubleVar(value=0.3)
        ttk.Entry(control, textvariable=self.density_var, width=5).pack(anchor="w")

        ttk.Button(control, text="Create Grid", command=self.create_grid).pack(fill=tk.X, pady=5)
        ttk.Button(control, text="Random Map", command=self.random_map).pack(fill=tk.X, pady=5)

        # ---- Canvas ----
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_click)

        self.grid_data = []
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None

        self.create_grid()

    def create_grid(self):
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()

        self.grid_data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.start = (self.rows - 2, self.cols - 3)
        self.goal = (self.rows - 3, 1)

        self.draw()

    def random_map(self):
        density = self.density_var.get()

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start or (r, c) == self.goal:
                    continue
                self.grid_data[r][c] = 1 if random.random() < density else 0

        self.draw()

    def on_click(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE

        if 0 <= r < self.rows and 0 <= c < self.cols:
            if (r, c) == self.start or (r, c) == self.goal:
                return
            self.grid_data[r][c] = 1 - self.grid_data[r][c]
            self.draw()

    def draw(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "white"

                if self.grid_data[r][c] == 1:
                    color = "black"

                if (r, c) == self.start:
                    color = "green"

                if (r, c) == self.goal:
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

                if (r, c) == self.start:
                    self.canvas.create_text(x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                                            text="S", fill="white", font=("Arial", 12, "bold"))

                if (r, c) == self.goal:
                    self.canvas.create_text(x1 + CELL_SIZE/2, y1 + CELL_SIZE/2,
                                            text="G", fill="white", font=("Arial", 12, "bold"))

        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()

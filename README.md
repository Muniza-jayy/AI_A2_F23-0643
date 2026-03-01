 AI2002 – Assignment 02
Informed Search with Dynamic Replanning
GOOD PERFORMANCE TIME APP
Overview

This project implements and visualizes Informed Search Algorithms in a dynamic grid environment.

Implemented algorithms:

Greedy Best-First Search (GBFS)

A* Search

The system allows:

Custom grid size

Adjustable obstacle density

Manual wall placement

Heuristic selection

Dynamic obstacle spawning

Real-time visualization

Performance metrics comparison

 Algorithms Implemented
1️Greedy Best-First Search

Evaluation function:

f(n) = h(n)

Expands node closest to goal heuristically

Fast but not optimal

2️⃣ A* Search

Evaluation function:

f(n) = g(n) + h(n)

Considers both path cost and heuristic

Guaranteed optimal (with admissible heuristic)

Heuristics

Manhattan Distance

Euclidean Distance

Both are admissible.

 Features

8-direction movement

Cost per action = 1

Dynamic obstacle spawning

Automatic replanning

Performance tracking:

Nodes Expanded

Path Cost

Execution Time

Number of Replans

🎮 GUI Controls

Left panel allows:

Rows / Columns input

Obstacle density control

Algorithm selection

Heuristic selection

Dynamic mode toggle

Spawn probability control

Create Grid

Random Map

Run

Clear Search

Exit

Visualization Colors
Element	Color
Start	Green
Goal	Red
Agent	Orange
Visited	Blue
Frontier	Yellow
Path	Lime
Walls	Black
📂 Project Structure
AI-A2_23F-0643
│
├── main.py
├── model.py
├── search.py
├── heuristics.py
├── README.md
└── report.pdf
⚙️ Requirements

Python 3.8+

Install Dependencies
pip install tkinter

(Note: Tkinter comes pre-installed with most Python distributions.)

▶️ How to Run

Navigate to project folder:

cd AI-A2_23F-0643

Run:

python main.py
Experimental Setup

Best Case:

Low obstacle density (0.1)

Minimal replanning

Worst Case:

High obstacle density (0.4+)

Dynamic obstacles enabled

Multiple replans

Screenshots and metrics included in report.

 Key Observations

GBFS expands fewer nodes in simple environments.

A* guarantees optimal path.

In dynamic environments, A* performs more reliably.

Heuristic quality directly affects performance.

Dynamic replanning increases realism.

Repository

GitHub Repository:


 Author

Muniza Jay
Roll No: 23F-0643
Artificial Intelligence – Assignment 02
"""
The task is to simulate an emergency network of cities connected by roads. 
Users can add cities and roads, simulate city failures, and visualize the network.
 The goal is to maintain connectivity among all active cities while minimizing 
 the total distance of roads used, even when some cities fail.
"""

"""The solution represents cities as nodes and roads as weighted edges in a graph. 
It allows interactive addition of cities and roads via a Tkinter GUI. City failures are simulated by marking nodes inactive. 
To ensure minimal connectivity among active cities, Kruskal’s algorithm computes the Minimum Spanning Tree,
 which is displayed visually. This approach combines graph algorithms with an interactive visualization for real-time emergency network planning."""

import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import defaultdict
import heapq

# =========================
# GRAPH LOGIC
# =========================
class Graph:
    def __init__(self):
        self.nodes = {}  # city -> {"x": X, "y": Y, "active": True/False}
        self.edges = []  # (weight, city1, city2, vulnerable)
        self.adj = defaultdict(list)

    # Add a city
    def add_city(self, name, x, y):
        if name in self.nodes:
            return False
        self.nodes[name] = {"x": x, "y": y, "active": True}
        return True

    # Add a road
    def add_road(self, a, b, w):
        if a not in self.nodes or b not in self.nodes:
            return False
        self.edges.append((w, a, b, False))
        self.adj[a].append((b, w))
        self.adj[b].append((a, w))
        return True

    # Mark a city as inactive (simulate failure)
    def deactivate_city(self, name):
        if name in self.nodes:
            self.nodes[name]["active"] = False

    # Mark an edge as vulnerable (Q2)
    def mark_vulnerable(self, a, b):
        for i, (w, x, y, v) in enumerate(self.edges):
            if (x == a and y == b) or (x == b and y == a):
                self.edges[i] = (w, x, y, True)

    # ---------- Kruskal MST (Q1) ----------
    def mst_kruskal(self):
        parent = {}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(a, b):
            parent[find(a)] = find(b)

        for n in self.nodes:
            if self.nodes[n]["active"]:
                parent[n] = n

        mst = []
        for w, a, b, _ in sorted(self.edges):
            if not self.nodes[a]["active"] or not self.nodes[b]["active"]:
                continue
            if find(a) != find(b):
                union(a, b)
                mst.append((a, b))
        return mst

    # ---------- Dijkstra shortest path (Q4) ----------
    def dijkstra(self, src):
        dist = {n: float("inf") for n in self.nodes}
        if not self.nodes.get(src, {}).get("active", False):
            return dist
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                if not self.nodes[v]["active"]:
                    continue
                if dist[v] > d + w:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    # ---------- Greedy Graph Coloring (Bonus) ----------
    def color_graph(self):
        color = {}
        for node in self.nodes:
            used = {color[n] for n, _ in self.adj[node] if n in color}
            c = 0
            while c in used:
                c += 1
            color[node] = c
        return color


# =========================
# COMMAND TREE (Q3)
# =========================
class CommandNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# Build balanced binary tree (for Q3)
def build_balanced_tree(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    root = CommandNode(arr[mid])
    root.left = build_balanced_tree(arr[:mid])
    root.right = build_balanced_tree(arr[mid + 1:])
    return root


# =========================
# GUI APPLICATION
# =========================
class EmergencyGUI:
    R = 15

    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title("Advanced Emergency Network Simulator")
        self.root.geometry("1100x650")

        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="lightgray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.save_click)

        # Side panel
        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # ----- Controls -----
        tk.Button(panel, text="Add City", command=self.add_city).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Add Road", command=self.add_road).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Show MST", command=self.show_mst).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Simulate Failure", command=self.fail_city).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Reliable Paths", command=self.reliable_paths).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Optimize Command Tree", command=self.optimize_tree).pack(fill=tk.X, pady=2)
        tk.Button(panel, text="Graph Coloring (Bonus)", command=self.color_graph).pack(fill=tk.X, pady=2)

        self.cx = self.cy = None
        self.root.mainloop()

    # =====================
    # Mouse click coordinates
    # =====================
    def save_click(self, event):
        self.cx, self.cy = event.x, event.y

    # =====================
    # Add city
    # =====================
    def add_city(self):
        if self.cx is None or self.cy is None:
            messagebox.showinfo("Info", "Click on canvas first")
            return
        name = simpledialog.askstring("City Name", "Enter city name:")
        if name and self.graph.add_city(name, self.cx, self.cy):
            self.redraw()
        elif name:
            messagebox.showerror("Error", "City already exists")

    # =====================
    # Add road
    # =====================
    def add_road(self):
        a = simpledialog.askstring("Road", "City A:")
        b = simpledialog.askstring("Road", "City B:")
        w = simpledialog.askfloat("Distance", "Enter distance:")
        if a and b and w is not None:
            if self.graph.add_road(a, b, w):
                self.redraw()

    # =====================
    # Show MST (Q1)
    # =====================
    def show_mst(self):
        self.redraw()
        mst_edges = self.graph.mst_kruskal()
        if not mst_edges:
            messagebox.showinfo("MST", "No MST available")
            return
        for a, b in mst_edges:
            self.draw_road(a, b, 0, color="green", width=4)
        messagebox.showinfo("MST", "Minimum Spanning Tree displayed (green edges)")

    # =====================
    # Simulate failure (Q4)
    # =====================
    def fail_city(self):
        name = simpledialog.askstring("Failure", "Disable which city?")
        if name not in self.graph.nodes:
            return
        self.graph.deactivate_city(name)
        self.redraw()
        active = [n for n in self.graph.nodes if self.graph.nodes[n]["active"]]
        if active:
            dist = self.graph.dijkstra(active[0])
            msg = "\n".join(f"{n}: {'∞' if dist[n]==float('inf') else dist[n]}" for n in dist)
            messagebox.showinfo("Shortest Paths", msg)

    # =====================
    # Reliable paths (Q2)
    # =====================
    def reliable_paths(self):
        a = simpledialog.askstring("Source", "From city:")
        b = simpledialog.askstring("Target", "To city:")
        if not a or not b or a not in self.graph.nodes or b not in self.graph.nodes:
            return
        self.graph.mark_vulnerable(a, b)
        self.redraw()
        messagebox.showinfo("Reliable Paths", f"Edge {a}-{b} marked vulnerable")

    # =====================
    # Command tree optimizer (Q3)
    # =====================
    def optimize_tree(self):
        cities = sorted(self.graph.nodes.keys())
        tree = build_balanced_tree(cities)
        messagebox.showinfo("Command Tree", "Command tree rebalanced (binary tree)")

    # =====================
    # Bonus: Graph coloring
    # =====================
    def color_graph(self):
        colors = self.graph.color_graph()
        palette = ["red", "green", "blue", "yellow", "purple"]
        for node, c in colors.items():
            self.canvas.create_text(self.graph.nodes[node]["x"], self.graph.nodes[node]["y"]-20,
                                    text=f"F{c}", fill=palette[c % len(palette)])
        messagebox.showinfo("Graph Coloring", "Greedy coloring applied (no adjacent hubs share frequency)")

    # =====================
    # Redraw canvas
    # =====================
    def redraw(self):
        self.canvas.delete("all")
        for w, a, b, vulnerable in self.graph.edges:
            self.draw_road(a, b, w, vulnerable)
        for n in self.graph.nodes:
            self.draw_city(n)

    def draw_city(self, name):
        city = self.graph.nodes[name]
        x, y = city["x"], city["y"]
        color = "blue" if city["active"] else "gray"
        self.canvas.create_oval(x - self.R, y - self.R, x + self.R, y + self.R, fill=color)
        self.canvas.create_text(x, y, text=name, fill="white")

    def draw_road(self, a, b, w, vulnerable=False, color="black", width=2):
        node_a = self.graph.nodes[a]
        node_b = self.graph.nodes[b]
        x1, y1 = node_a["x"], node_a["y"]
        x2, y2 = node_b["x"], node_b["y"]
        if vulnerable:
            color = "red"
        elif not node_a["active"] or not node_b["active"]:
            color = "gray"
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        mx, my = (x1+x2)/2, (y1+y2)/2
        self.canvas.create_text(mx, my, text=str(w), fill="darkred")


# =========================
# RUN
# =========================
EmergencyGUI()

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



class Graph:
    def __init__(self):
        self.nodes = {}          # city -> {x, y, active}
        self.edges = []          # (weight, city1, city2)
        self.adj = defaultdict(list)

    def add_city(self, name, x, y):
        if name in self.nodes:
            return False
        self.nodes[name] = {"x": x, "y": y, "active": True}
        return True

    def add_road(self, a, b, weight):
        if a not in self.nodes or b not in self.nodes:
            return False
        self.edges.append((weight, a, b))
        self.adj[a].append((b, weight))
        self.adj[b].append((a, weight))
        return True

    def deactivate_city(self, name):
        if name in self.nodes:
            self.nodes[name]["active"] = False

   
    def mst_kruskal(self):
        parent = {n: n for n in self.nodes if self.nodes[n]["active"]}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            parent[find(a)] = find(b)

        mst = []
        for w, a, b in sorted(self.edges):
            if not self.nodes[a]["active"] or not self.nodes[b]["active"]:
                continue
            if find(a) != find(b):
                union(a, b)
                mst.append((a, b))
        return mst



class EmergencyGUI:
    R = 15

    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title("Emergency Network Simulator")
        self.root.geometry("900x600")

        self.canvas = tk.Canvas(self.root, bg="lightgray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.save_click)

        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Button(panel, text="Add City", command=self.add_city).pack(fill=tk.X, pady=5)
        tk.Button(panel, text="Add Road", command=self.add_road).pack(fill=tk.X, pady=5)
        tk.Button(panel, text="Show MST", command=self.show_mst).pack(fill=tk.X, pady=5)
        tk.Button(panel, text="Simulate Failure", command=self.fail_city).pack(fill=tk.X, pady=5)

        self.cx = self.cy = None
        self.root.mainloop()

    
    def save_click(self, e):
        self.cx, self.cy = e.x, e.y

    def add_city(self):
        if self.cx is None:
            messagebox.showinfo("Info", "Click on canvas first")
            return
        name = simpledialog.askstring("City", "City name:")
        if not name:
            return
        if self.graph.add_city(name, self.cx, self.cy):
            self.redraw()
        else:
            messagebox.showerror("Error", "City already exists")

    
    def add_road(self):
        a = simpledialog.askstring("Road", "First city:")
        b = simpledialog.askstring("Road", "Second city:")
        if not a or not b:
            return
        w = simpledialog.askfloat("Weight", "Distance:")
        if w is None:
            return
        if self.graph.add_road(a, b, w):
            self.redraw()

    
    def show_mst(self):
        self.redraw()
        for a, b in self.graph.mst_kruskal():
            self.draw_road(a, b, color="green", width=4)

    def fail_city(self):
        name = simpledialog.askstring("Failure", "City to deactivate:")
        if name in self.graph.nodes:
            self.graph.deactivate_city(name)
            self.redraw()

   
    def redraw(self):
        self.canvas.delete("all")

        # Draw roads
        for w, a, b in self.graph.edges:
            self.draw_road(a, b)

        # Draw cities
        for name in self.graph.nodes:
            self.draw_city(name)

    def draw_city(self, name):
        n = self.graph.nodes[name]
        x, y = n["x"], n["y"]
        color = "gray" if not n["active"] else "blue"
        self.canvas.create_oval(
            x - self.R, y - self.R, x + self.R, y + self.R, fill=color
        )
        self.canvas.create_text(x, y, text=name, fill="white")

    def draw_road(self, a, b, color="black", width=2):
        if not self.graph.nodes[a]["active"] or not self.graph.nodes[b]["active"]:
            color = "gray"

        x1, y1 = self.graph.nodes[a]["x"], self.graph.nodes[a]["y"]
        x2, y2 = self.graph.nodes[b]["x"], self.graph.nodes[b]["y"]

        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

        # Draw weight at midpoint
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        for w, c1, c2 in self.graph.edges:
            if (c1 == a and c2 == b) or (c1 == b and c2 == a):
                self.canvas.create_text(mx, my, text=str(w), fill="red")
                break


EmergencyGUI()

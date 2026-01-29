import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import math
from collections import defaultdict

# -------------------------
# Graph Class
# -------------------------
class Graph:
    def __init__(self):
        self.nodes = {}  # name: {"x": , "y": , "type": , "active": }
        self.edges = []  # (weight, u_name, v_name)
        self.adj = defaultdict(list)

    def add_node(self, name, x, y, type_="normal"):
        if name in self.nodes:
            return False
        self.nodes[name] = {"x": x, "y": y, "type": type_, "active": True}
        return True

    def add_edge(self, u, v, weight):
        if u not in self.nodes or v not in self.nodes:
            return False
        self.edges.append((weight, u, v))
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        return True

    def remove_node(self, name):
        if name not in self.nodes: return
        self.nodes[name]["active"] = False
        for neighbor, _ in self.adj[name]:
            self.adj[neighbor] = [(n, w) for n, w in self.adj[neighbor] if n != name]
        self.adj[name] = []

    def kruskal_mst(self):
        parent = {}
        for node in self.nodes:
            parent[node] = node

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            parent[find(u)] = find(v)

        mst = []
        for w, u, v in sorted(self.edges):
            if not self.nodes[u]["active"] or not self.nodes[v]["active"]:
                continue
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
        return mst

# -------------------------
# GUI Class
# -------------------------
class EmergencyNetworkGUI:
    NODE_RADIUS = 15

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Emergency Network Simulator with Custom Edge Weights")
        self.root.geometry("1000x700")
        self.graph = Graph()
        self.click_x, self.click_y = None, None

        # Canvas
        self.canvas = tk.Canvas(self.root, width=700, height=700, bg="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

        # Control Panel
        self.control_panel = ttk.Frame(self.root, padding=10)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(self.control_panel, text="Emergency Network Controls", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Button(self.control_panel, text="Add City", command=self.add_city).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_panel, text="Add Road", command=self.add_road).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_panel, text="Generate MST", command=self.show_mst).pack(fill=tk.X, pady=5)
        ttk.Button(self.control_panel, text="Simulate Failure", command=self.simulate_failure).pack(fill=tk.X, pady=5)

        # Status bar
        self.status = ttk.Label(self.root, text="Click to place city", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.mainloop()

    # -------------------------
    # GUI Actions
    # -------------------------
    def on_click(self, event):
        self.click_x, self.click_y = event.x, event.y
        self.status.config(text=f"Click at ({self.click_x}, {self.click_y})")

    def add_city(self):
        if self.click_x is None or self.click_y is None:
            messagebox.showinfo("Info", "Click on canvas first to place city")
            return
        city_name = simpledialog.askstring("City Name", "Enter city/node name:")
        if not city_name: return
        if not self.graph.add_node(city_name, self.click_x, self.click_y):
            messagebox.showerror("Error", f"City '{city_name}' already exists")
            return
        self.draw_node(city_name)

    def add_road(self):
        if len(self.graph.nodes) < 2:
            messagebox.showinfo("Info", "Need at least 2 cities to add a road")
            return
        # Ask user to input the names of two cities
        u = simpledialog.askstring("Road", "Enter first city name:")
        v = simpledialog.askstring("Road", "Enter second city name:")
        if not u or not v:
            return
        if u not in self.graph.nodes or v not in self.graph.nodes:
            messagebox.showerror("Error", "One or both cities do not exist")
            return
        if u == v:
            messagebox.showerror("Error", "Cannot connect a city to itself")
            return
        # Ask for custom weight
        weight = simpledialog.askfloat("Road Weight", f"Enter weight/distance for road {u}-{v}:")
        if weight is None:
            return
        self.graph.add_edge(u, v, weight)
        self.draw_edge(u, v)

    def show_mst(self):
        if len(self.graph.nodes) < 2:
            messagebox.showinfo("Info", "Need at least 2 cities to compute MST")
            return
        mst = self.graph.kruskal_mst()
        for u, v, w in mst:
            self.draw_edge(u, v, color="green", width=3)

    def simulate_failure(self):
        active_nodes = [name for name, info in self.graph.nodes.items() if info["active"]]
        if not active_nodes: return
        # Let user select city to fail
        city_name = simpledialog.askstring("Failure Simulation", "Enter city name to fail:")
        if city_name not in self.graph.nodes or not self.graph.nodes[city_name]["active"]:
            messagebox.showerror("Error", "Invalid or inactive city")
            return
        self.graph.remove_node(city_name)
        self.draw_node(city_name)

    # -------------------------
    # Drawing Utilities
    # -------------------------
    def draw_node(self, name):
        node = self.graph.nodes[name]
        x, y = node["x"], node["y"]
        color = "gray" if not node["active"] else "blue"
        self.canvas.create_oval(x - self.NODE_RADIUS, y - self.NODE_RADIUS,
                                x + self.NODE_RADIUS, y + self.NODE_RADIUS, fill=color, outline="black", width=2)
        self.canvas.create_text(x, y, text=name, fill="white", font=("Arial", 10, "bold"))

    def draw_edge(self, u, v, color="black", width=2):
        x1, y1 = self.graph.nodes[u]["x"], self.graph.nodes[u]["y"]
        x2, y2 = self.graph.nodes[v]["x"], self.graph.nodes[v]["y"]
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

# -------------------------
# Run the GUI
# -------------------------
if __name__ == "__main__":
    EmergencyNetworkGUI()

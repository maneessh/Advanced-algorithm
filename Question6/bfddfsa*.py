"""You want to find a path between two cities (Glogow → Plock) in a road network. The network is represented as a directed, weighted graph where:
Nodes are cities.
Edges are roads with distances.
You want to compare different search algorithms (DFS, BFS, A*) to see how they traverse the network and which path each finds."""

"""Graph Representation:
graph dictionary stores neighbors and road distances.
heuristic dictionary provides estimated straight-line distance to the goal (for A*).
Algorithms Implemented:
DFS (Depth-First Search):
Explores as far as possible along each branch before backtracking.
Uses a stack; path may not be shortest.
BFS (Breadth-First Search):
Explores all neighbors level by level.
Uses a queue; finds shortest path in terms of edges.
A Search:*
Combines actual distance so far (g) + estimated distance to goal (h).
Uses a priority queue; finds shortest path considering weights.
Visualization:
Uses NetworkX to create a directed graph.
Matplotlib draws the network and highlights the path found by each algorithm.
Each algorithm’s path is shown in a different color: DFS (blue), BFS (green), A* (red).
Edge weights are labeled for clarity."""
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import heapq

# ---------- Graph ----------
graph = {
    'Glogow': [('Leszno', 45), ('Wroclaw', 130)],
    'Leszno': [('Poznan', 90), ('Kalisz', 100), ('Wroclaw', 87)],
    'Poznan': [('Bydgoszcz', 140), ('Konin', 130)],
    'Wroclaw': [('Opole', 100)],
    'Kalisz': [('Konin', 120), ('Czestochowa', 160), ('Lodz', 165)],
    'Konin': [('Wloclawek', 120), ('Lodz', 150)],
    'Bydgoszcz': [('Wloclawek', 110)],
    'Wloclawek': [('Plock', 55)],
    'Opole': [('Czestochowa', 118)],
    'Czestochowa': [('Lodz', 128), ('Katowice', 80)],
    'Lodz': [('Warsaw', 130), ('Radom', 82)],
    'Plock': [],
    'Warsaw': [],
    'Katowice': [('Krakow', 85)],
    'Radom': [('Kielce', 120)],
    'Kielce': [('Krakow', 102)],
    'Krakow': []
}

heuristic = {
    'Glogow': 280, 'Leszno': 240, 'Poznan': 180, 'Wroclaw': 280,
    'Kalisz': 190, 'Konin': 150, 'Bydgoszcz': 110, 'Wloclawek': 65,
    'Opole': 265, 'Czestochowa': 220, 'Lodz': 160, 'Plock': 0,
    'Warsaw': 95, 'Katowice': 270, 'Radom': 140, 'Kielce': 180, 'Krakow': 250
}

start = "Glogow"
goal = "Plock"

# ---------- DFS, BFS, A* ----------
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor, _ in reversed(graph.get(node, [])):
            stack.append((neighbor, path + [neighbor]))
    return None

def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor, _ in graph.get(node, []):
            queue.append((neighbor, path + [neighbor]))
    return None

def a_star(graph, start, goal, h):
    pq = [(h[start], 0, start, [start])]
    visited = set()
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + h[neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
    return None

dfs_path = dfs(graph, start, goal)
bfs_path = bfs(graph, start, goal)
astar_path = a_star(graph, start, goal, heuristic)

# ---------- NetworkX Graph ----------
G = nx.DiGraph()
for node, neighbors in graph.items():
    for neighbor, weight in neighbors:
        G.add_edge(node, neighbor, weight=weight)

# Use Kamada-Kawai layout for better spacing
pos = nx.kamada_kawai_layout(G)

# ---------- Function to draw individual path ----------
def draw_path(path, color, title):
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightblue', arrowsize=20)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Highlight the path
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=4, arrows=True)
    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.show()

# ---------- Draw each algorithm on a separate page ----------
draw_path(dfs_path, 'blue', 'DFS Path (Blue) from Glogow → Plock')
draw_path(bfs_path, 'green', 'BFS Path (Green) from Glogow → Plock')
draw_path(astar_path, 'red', 'A* Path (Red) from Glogow → Plock')

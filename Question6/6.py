from collections import deque
import heapq

# -------------------------
# Graph (City : [(Neighbor, Distance)])
# -------------------------
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

# -------------------------
# Heuristic values (straight-line distance to Plock)
# -------------------------
heuristic = {
    'Glogow': 280, 'Leszno': 240, 'Poznan': 180, 'Wroclaw': 280,
    'Kalisz': 190, 'Konin': 150, 'Bydgoszcz': 110, 'Wloclawek': 65,
    'Opole': 265, 'Czestochowa': 220, 'Lodz': 160, 'Plock': 0,
    'Warsaw': 95, 'Katowice': 270, 'Radom': 140, 'Kielce': 180, 'Krakow': 250
}

# -------------------------
# DFS
# -------------------------
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

# -------------------------
# BFS
# -------------------------
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

# -------------------------
# A* Search
# -------------------------
def a_star(graph, start, goal, h):
    pq = [(h[start], 0, start, [start])]
    visited = set()

    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path, g
        if node in visited:
            continue
        visited.add(node)
        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + h[neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
    return None, float('inf')

# -------------------------
# Distance Calculation
# -------------------------
def path_distance(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for n, d in graph[path[i]]:
            if n == path[i+1]:
                total += d
    return total

# -------------------------
# Run Program
# -------------------------
start = "Glogow"
goal = "Plock"

dfs_path = dfs(graph, start, goal)
bfs_path = bfs(graph, start, goal)
astar_path, astar_cost = a_star(graph, start, goal, heuristic)

print("DFS Path:", dfs_path)
print("DFS Distance:", path_distance(graph, dfs_path))

print("\nBFS Path:", bfs_path)
print("BFS Distance:", path_distance(graph, bfs_path))

print("\nA* Path:", astar_path)
print("A* Distance:", astar_cost)

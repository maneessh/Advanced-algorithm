
"""
Task 6: Polish Cities Routing Problem
Solving using DFS, BFS, and A* algorithms
Start: Glogow (blue node)
Goal: Plock (red node)
"""

from collections import deque
import heapq

# Graph representation from diagram (a)
graph_a = {
    'Glogow': [('Leszno', 45), ('Wroclaw', 130)],
    'Leszno': [('Glogow', 45), ('Poznan', 90), ('Kalisz', 100), ('Wroclaw', 87)],
    'Poznan': [('Leszno', 90), ('Bydgoszcz', 140), ('Konin', 130)],
    'Wroclaw': [('Glogow', 130), ('Leszno', 87), ('Opole', 100)],
    'Kalisz': [('Leszno', 100), ('Konin', 120), ('Czestochowa', 160), ('Lodz', 165)],
    'Konin': [('Poznan', 130), ('Kalisz', 120), ('Wloclawek', 120), ('Lodz', 150)],
    'Bydgoszcz': [('Poznan', 140), ('Wloclawek', 110)],
    'Wloclawek': [('Bydgoszcz', 110), ('Konin', 120), ('Plock', 55)],
    'Opole': [('Wroclaw', 100), ('Czestochowa', 118)],
    'Czestochowa': [('Opole', 118), ('Kalisz', 160), ('Lodz', 128), ('Katowice', 80)],
    'Lodz': [('Kalisz', 165), ('Konin', 150), ('Czestochowa', 128), ('Warsaw', 130), ('Radom', 82)],
    'Plock': [('Wloclawek', 55), ('Warsaw', 105)],
    'Warsaw': [('Plock', 105), ('Lodz', 130), ('Radom', 91)],
    'Katowice': [('Czestochowa', 80), ('Krakow', 85)],
    'Radom': [('Lodz', 82), ('Warsaw', 91), ('Kielce', 120)],
    'Kielce': [('Radom', 120), ('Krakow', 102)],
    'Krakow': [('Katowice', 85), ('Kielce', 102)]
}

# Straight-line distances (heuristic) from diagram (b)
heuristic = {
    'Glogow': 280,
    'Leszno': 240,
    'Poznan': 180,
    'Wroclaw': 280,
    'Kalisz': 190,
    'Konin': 150,
    'Bydgoszcz': 110,
    'Wloclawek': 65,
    'Opole': 265,
    'Czestochowa': 220,
    'Lodz': 160,
    'Plock': 0,  # Goal node
    'Warsaw': 95,
    'Katowice': 270,
    'Radom': 140,
    'Kielce': 180,
    'Krakow': 250
}


def dfs(graph, start, goal):
    """
    Depth-First Search Algorithm
    Returns: path, nodes_explored, open_closed_trace
    """
    open_list = [(start, [start])]  # Stack: (node, path)
    closed_set = set()
    trace = []
    
    print("=== DEPTH-FIRST SEARCH (DFS) ===\n")
    iteration = 0
    
    while open_list:
        iteration += 1
        current, path = open_list.pop()  # Pop from end (stack behavior)
        
        trace.append({
            'iteration': iteration,
            'current': current,
            'open': [node for node, _ in open_list],
            'closed': list(closed_set),
            'path_so_far': path
        })
        
        print(f"Iteration {iteration}:")
        print(f"  Current Node: {current}")
        print(f"  Open: {[node for node, _ in open_list]}")
        print(f"  Closed: {list(closed_set)}")
        print(f"  Path so far: {' -> '.join(path)}")
        
        if current == goal:
            print(f"\n✓ Goal reached: {goal}")
            print(f"  Final path: {' -> '.join(path)}")
            total_distance = calculate_path_distance(graph, path)
            print(f"  Total distance: {total_distance} km\n")
            return path, len(closed_set) + 1, trace, total_distance
        
        if current in closed_set:
            print(f"  Node already visited, skipping.\n")
            continue
        
        closed_set.add(current)
        
        # Add neighbors to stack (in reverse to maintain left-to-right exploration)
        neighbors = [(neighbor, path + [neighbor]) 
                    for neighbor, _ in reversed(graph.get(current, []))]
        
        for neighbor, new_path in neighbors:
            if neighbor not in closed_set:
                open_list.append((neighbor, new_path))
        
        print(f"  Added neighbors: {[n for n, _ in neighbors]}\n")
    
    print("✗ No path found\n")
    return None, len(closed_set), trace, float('inf')


def bfs(graph, start, goal):
    """
    Breadth-First Search Algorithm
    Returns: path, nodes_explored, open_closed_trace
    """
    open_queue = deque([(start, [start])])  # Queue: (node, path)
    closed_set = set()
    trace = []
    
    print("=== BREADTH-FIRST SEARCH (BFS) ===\n")
    iteration = 0
    
    while open_queue:
        iteration += 1
        current, path = open_queue.popleft()  # Pop from front (queue behavior)
        
        trace.append({
            'iteration': iteration,
            'current': current,
            'open': [node for node, _ in open_queue],
            'closed': list(closed_set),
            'path_so_far': path
        })
        
        print(f"Iteration {iteration}:")
        print(f"  Current Node: {current}")
        print(f"  Open: {[node for node, _ in open_queue]}")
        print(f"  Closed: {list(closed_set)}")
        print(f"  Path so far: {' -> '.join(path)}")
        
        if current == goal:
            print(f"\n✓ Goal reached: {goal}")
            print(f"  Final path: {' -> '.join(path)}")
            total_distance = calculate_path_distance(graph, path)
            print(f"  Total distance: {total_distance} km\n")
            return path, len(closed_set) + 1, trace, total_distance
        
        if current in closed_set:
            print(f"  Node already visited, skipping.\n")
            continue
        
        closed_set.add(current)
        
        # Add neighbors to queue
        for neighbor, _ in graph.get(current, []):
            if neighbor not in closed_set and not any(neighbor == n for n, _ in open_queue):
                open_queue.append((neighbor, path + [neighbor]))
        
        print(f"  Added neighbors to queue\n")
    
    print("✗ No path found\n")
    return None, len(closed_set), trace, float('inf')


def a_star(graph, start, goal, heuristic_func):
    """
    A* Search Algorithm
    Returns: path, nodes_explored, open_closed_trace
    """
    # Priority queue: (f_cost, g_cost, node, path)
    open_heap = [(heuristic_func[start], 0, start, [start])]
    closed_set = set()
    g_costs = {start: 0}
    trace = []
    
    print("=== A* SEARCH ===\n")
    iteration = 0
    
    while open_heap:
        iteration += 1
        f_cost, g_cost, current, path = heapq.heappop(open_heap)
        h_cost = f_cost - g_cost
        
        trace.append({
            'iteration': iteration,
            'current': current,
            'g_cost': g_cost,
            'h_cost': h_cost,
            'f_cost': f_cost,
            'open': [(n, f) for f, _, n, _ in open_heap],
            'closed': list(closed_set),
            'path_so_far': path
        })
        
        print(f"Iteration {iteration}:")
        print(f"  Current Node: {current}")
        print(f"  g(n) = {g_cost}, h(n) = {h_cost}, f(n) = {f_cost}")
        print(f"  Open: {[(n, f) for f, _, n, _ in sorted(open_heap)]}")
        print(f"  Closed: {list(closed_set)}")
        print(f"  Path so far: {' -> '.join(path)}")
        
        if current == goal:
            print(f"\n✓ Goal reached: {goal}")
            print(f"  Final path: {' -> '.join(path)}")
            print(f"  Total distance (g-cost): {g_cost} km\n")
            return path, len(closed_set) + 1, trace, g_cost
        
        if current in closed_set:
            print(f"  Node already visited, skipping.\n")
            continue
        
        closed_set.add(current)
        
        # Explore neighbors
        for neighbor, edge_cost in graph.get(current, []):
            if neighbor in closed_set:
                continue
            
            tentative_g = g_cost + edge_cost
            
            # Check if this path to neighbor is better
            if neighbor not in g_costs or tentative_g < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g
                h = heuristic_func[neighbor]
                f = tentative_g + h
                new_path = path + [neighbor]
                heapq.heappush(open_heap, (f, tentative_g, neighbor, new_path))
                print(f"  Added/Updated {neighbor}: g={tentative_g}, h={h}, f={f}")
        
        print()
    
    print("✗ No path found\n")
    return None, len(closed_set), trace, float('inf')


def calculate_path_distance(graph, path):
    """Calculate total distance of a path"""
    if not path or len(path) < 2:
        return 0
    
    total = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        for neighbor, distance in graph.get(current, []):
            if neighbor == next_node:
                total += distance
                break
    return total


def print_comparison(dfs_result, bfs_result, astar_result):
    """Print comparison of all three algorithms"""
    print("\n" + "="*80)
    print("ALGORITHM COMPARISON")
    print("="*80 + "\n")
    
    algorithms = [
        ("DFS", dfs_result),
        ("BFS", bfs_result),
        ("A*", astar_result)
    ]
    
    print(f"{'Algorithm':<15} {'Path Found':<15} {'Distance (km)':<15} {'Nodes Explored':<15}")
    print("-" * 80)
    
    for name, (path, nodes, _, distance) in algorithms:
        path_str = "Yes" if path else "No"
        dist_str = f"{distance}" if distance != float('inf') else "N/A"
        print(f"{name:<15} {path_str:<15} {dist_str:<15} {nodes:<15}")
    
    print("\n" + "="*80)
    print("PATH DETAILS")
    print("="*80 + "\n")
    
    for name, (path, _, _, distance) in algorithms:
        print(f"{name} Path:")
        if path:
            print(f"  {' -> '.join(path)}")
            print(f"  Distance: {distance} km")
        else:
            print(f"  No path found")
        print()


if __name__ == "__main__":
    start_city = 'Glogow'
    goal_city = 'Plock'
    
    print("="*80)
    print("POLISH CITIES ROUTING PROBLEM")
    print("="*80)
    print(f"Start City: {start_city} (Blue Node)")
    print(f"Goal City: {goal_city} (Red Node)")
    print("="*80 + "\n")
    
    # Run DFS
    dfs_result = dfs(graph_a, start_city, goal_city)
    print("\n" + "="*80 + "\n")
    
    # Run BFS
    bfs_result = bfs(graph_a, start_city, goal_city)
    print("\n" + "="*80 + "\n")
    
    # Run A*
    astar_result = a_star(graph_a, start_city, goal_city, heuristic)
    
    # Print comparison
    print_comparison(dfs_result, bfs_result, astar_result)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

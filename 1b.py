import random
import math

# -----------------------------
# Generate random cities
# -----------------------------
def generate_cities(n, limit=1000):
    return [(random.uniform(0, limit), random.uniform(0, limit)) for _ in range(n)]

# -----------------------------
# Distance calculation
# -----------------------------
def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def total_distance(tour, cities):
    dist = 0
    for i in range(len(tour)):
        dist += euclidean(cities[tour[i]], cities[tour[(i+1) % len(tour)]])
    return dist

# -----------------------------
# Neighborhood operators
# -----------------------------
def swap_neighbor(tour):
    a, b = random.sample(range(len(tour)), 2)
    new_tour = tour[:]
    new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
    return new_tour

def two_opt_neighbor(tour):
    a, b = sorted(random.sample(range(len(tour)), 2))
    return tour[:a] + list(reversed(tour[a:b])) + tour[b:]

# -----------------------------
# Simulated Annealing
# -----------------------------
def simulated_annealing(cities, cooling="exponential",
                         T_initial=1000, alpha=0.995, beta=0.1,
                         T_min=1e-3, max_iter=10000):

    n = len(cities)
    current_tour = list(range(n))
    random.shuffle(current_tour)

    current_cost = total_distance(current_tour, cities)
    best_tour = current_tour[:]
    best_cost = current_cost

    T = T_initial

    for k in range(max_iter):
        if T < T_min:
            break

        # Choose neighborhood method
        if random.random() < 0.5:
            new_tour = swap_neighbor(current_tour)
        else:
            new_tour = two_opt_neighbor(current_tour)

        new_cost = total_distance(new_tour, cities)
        delta = new_cost - current_cost

        # Acceptance rule
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = new_tour
            current_cost = new_cost

            if current_cost < best_cost:
                best_tour = current_tour[:]
                best_cost = current_cost

        # Cooling schedule
        if cooling == "exponential":
            T *= alpha
        elif cooling == "linear":
            T -= beta

    return best_tour, best_cost


# Create TSP instance
N = 30
cities = generate_cities(N)

# Exponential cooling
tour_exp, cost_exp = simulated_annealing(
    cities, cooling="exponential")

# Linear cooling
tour_lin, cost_lin = simulated_annealing(
    cities, cooling="linear")

print("Exponential Cooling Distance:", round(cost_exp, 2))
print("Linear Cooling Distance:", round(cost_lin, 2))

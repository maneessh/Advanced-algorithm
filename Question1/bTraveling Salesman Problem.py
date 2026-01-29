
""" problem : Find an approximately shortest route visiting all cities once
 (Traveling Salesman Problem) using heuristic optimization."""
import random
import math


# Step 1 Creating random cities x , y cordinates
def generate_cities(n, limit=1000):
   
    # Generates n no of cities with random x, y coordinates on limits
    cities = []
    for _ in range(n):
        x = random.uniform(0, limit)
        y = random.uniform(0, limit)
        cities.append((x, y))
    return cities



# Step 2 Distance calculations
def euclidean(city1, city2):

    # Calculates Euclidean distance 
    return math.sqrt(
        (city1[0] - city2[0]) ** 2 +
        (city1[1] - city2[1]) ** 2
    )


def total_distance(tour, cities):
  
    # Camputes the total distance of a TSP tour (Tour is Circular)= last city = first
    distance = 0
    for i in range(len(tour)):
        current_city = cities[tour[i]]
        next_city = cities[tour[(i + 1) % len(tour)]]
        distance += euclidean(current_city, next_city)
    return distance



# Step 3 Neighborhood generates methods
def swap_neighbor(tour):
  
    # Genrates a neighbot by swapping random two cities
    a, b = random.sample(range(len(tour)), 2)
    new_tour = tour[:]
    new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
    return new_tour

  #Generates a neighbor using the 2-opt method,
   # which reverses a segment of the tour.
def two_opt_neighbor(tour):

    a, b = sorted(random.sample(range(len(tour)), 2))
    return tour[:a] + list(reversed(tour[a:b])) + tour[b:]


# --------------------------------------------------
# Step 4: Simulated Annealing algorithm
# --------------------------------------------------
def simulated_annealing(
    cities,
    cooling="exponential",
    T_initial=1000,
    alpha=0.995,
    beta=0.1,
    T_min=1e-3,
    max_iter=10000
):
    #Solves the Traveling salesman problem using simlated annealing

    n = len(cities)

    # Initial random solution
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = total_distance(current_tour, cities)

    # Best solution found so far
    best_tour = current_tour[:]
    best_cost = current_cost

    # Initial temperature
    T = T_initial

    for _ in range(max_iter):
        if T < T_min:
            break

        # Choose neighborhood strategy randomly
        if random.random() < 0.5:
            new_tour = swap_neighbor(current_tour)
        else:
            new_tour = two_opt_neighbor(current_tour)

        new_cost = total_distance(new_tour, cities)
        delta = new_cost - current_cost

        # Acceptance condition
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = new_tour
            current_cost = new_cost

            # Update best solution
            if current_cost < best_cost:
                best_tour = current_tour[:]
                best_cost = current_cost

        # Cooling schedule
        if cooling == "exponential":
            T *= alpha
        elif cooling == "linear":
            T -= beta

    return best_tour, best_cost


# --------------------------------------------------
# Step 5: Run the algorithm
# --------------------------------------------------
N = 30
cities = generate_cities(N)

# Exponential cooling
tour_exp, cost_exp = simulated_annealing(cities, cooling="exponential")

# Linear cooling
tour_lin, cost_lin = simulated_annealing(cities, cooling="linear")

print("Exponential Cooling Distance:", round(cost_exp, 2))
print("Linear Cooling Distance:", round(cost_lin, 2))

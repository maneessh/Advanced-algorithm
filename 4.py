# Step 0: Input data (arrays)
demand = [
    [20, 15, 25],  # Hour 06
    [22, 16, 28],  # Hour 07
    [25, 18, 30],  # Hour 08
    [30, 20, 35],  # Hour 09
]

hours = [6, 7, 8, 9]

sources = [
    ['S1', 'Solar', 50, 6, 18, 1.0],
    ['S2', 'Hydro', 40, 0, 24, 1.5],
    ['S3', 'Diesel', 60, 17, 23, 3.0],
]

districts = ['A', 'B', 'C']

# Step 1: Greedy allocation function
def greedy_allocate(hour_index):
    demand_hour = demand[hour_index]
    hour = hours[hour_index]
    allocation = [[0]*len(sources) for _ in range(len(districts))]
    remaining_caps = [s[2] for s in sources]  # capacities per source

    # Sort sources by cost (greedy)
    sorted_indices = sorted(range(len(sources)), key=lambda i: sources[i][5])

    for d_idx, req in enumerate(demand_hour):
        remaining = req
        for s_idx in sorted_indices:
            s = sources[s_idx]
            if s[3] <= hour <= s[4] and remaining_caps[s_idx] > 0:
                used = min(remaining, remaining_caps[s_idx])
                allocation[d_idx][s_idx] = used
                remaining -= used
                remaining_caps[s_idx] -= used
            if remaining <= 0.1*req:  # ±10% flexibility
                break
    return allocation

# Step 2: Print detailed allocation for all hours
total_cost = 0
total_energy = 0
renewable_energy = 0
diesel_usage = []

print("Step-by-Step Allocation Report for All Hours (with cost per source):\n")

for h_idx, hour in enumerate(hours):
    alloc = greedy_allocate(h_idx)
    print(f"Hour {hour}:")
    print(f"{'District':<10}{'Demand':<10}{'Solar(kWh)':<12}{'Cost(Rs)':<12}{'Hydro(kWh)':<12}{'Cost(Rs)':<12}{'Diesel(kWh)':<14}{'Cost(Rs)':<12}{'Total(kWh)':<12}{'Total Cost(Rs)':<15}")
    
    total_cost_hour = 0  # total cost for this hour

    for d_idx, district in enumerate(districts):
        solar = alloc[d_idx][0]
        hydro = alloc[d_idx][1]
        diesel = alloc[d_idx][2]

        solar_cost = solar * 1.0
        hydro_cost = hydro * 1.5
        diesel_cost = diesel * 3.0

        total_supplied = solar + hydro + diesel
        district_cost = solar_cost + hydro_cost + diesel_cost
        total_cost_hour += district_cost

        total_energy += total_supplied
        total_cost += district_cost
        renewable_energy += solar + hydro
        if diesel > 0:
            diesel_usage.append((hour, district))
        
        print(f"{district:<10}{demand[h_idx][d_idx]:<10}{solar:<12}{solar_cost:<12}{hydro:<12}{hydro_cost:<12}{diesel:<14}{diesel_cost:<12}{total_supplied:<12}{district_cost:<15}")

    print(f"Total Cost for Hour {hour}: Rs. {total_cost_hour:.2f}\n")
    
# Step 3: Summary
print(f"Overall Total Cost of Distribution: Rs. {total_cost:.2f}")
print(f"% of Energy Fulfilled by Renewable Sources: {renewable_energy/total_energy*100:.1f}%")
if diesel_usage:
    print("Diesel was used at hours/districts:")
    for h, d in diesel_usage:
        print(f"  Hour {h}, District {d}")
else:
    print("No Diesel was used.")

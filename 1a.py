import math

"""calculating the total distance from the hub (x,y) to all the sensor point"""

def calculate_total_distance(hub_x, hub_y , sensor_point):
    total_dist = 0

    for sensor_x,sensor_y in sensor_point:
        distance = math.sqrt((hub_x - sensor_x) ** 2 +
                             (hub_y - sensor_y) ** 2)
        total_dist += distance
    return total_dist

"""Finding the best loactiion for the hub so that the total distance to all
sensors is minimized"""

def find_best_hub_location(sensor_points):
    # if there are no sensors, distance is zero
    if not sensor_points:
        return 0
    
    #step 1 : start from the center point
    hub_x = 0
    hub_y = 0

    for x, y in sensor_points:
        hub_x += x
        hub_y += y

    hub_x /= len(sensor_points)
    hub_y /= len(sensor_points)

    #step 2: Gradually improve hub position
    for _ in range(1000):
        weighted_x_sum = 0
        weighted_y_sum = 0
        weight_total = 0

        for sensor_x, sensor_y in sensor_points:
            dist = math.sqrt((hub_x - sensor_x) **2 +
                             (hub_y - sensor_y) ** 2)
            
            #if hub lands exactly on a sensor, stop
            if dist == 0:
                return calculate_total_distance(hub_x,hub_y, sensor_points)
            
            weight = 1 / dist
            weighted_x_sum += weight * sensor_x
            weighted_y_sum += weight * sensor_y
            weight_total += weight

        new_hub_x = weighted_x_sum / weight_total
        new_hub_y = weighted_y_sum / weight_total

        #Stoppping if the hub bearly moves anymore
        movement = math.sqrt((new_hub_x - hub_x) ** 2 +
                             (new_hub_y - hub_y) ** 2)
        
        if movement < 0.000001:
            hub_x, hub_y = new_hub_x, new_hub_y
            break
        
        hub_x, hub_y = new_hub_x, new_hub_y


    #step 3: Return minimum total distance
    return calculate_total_distance(hub_x, hub_y, sensor_points)

#USER INPUT
num_sensors = int(input("Enter number of sensors:"))

sensor_points = []

for i in range(num_sensors):
    print(f"Enter co-ordinates of sensor {i + 1}:")
    x = float(input(" x: "))
    y = float(input(" y : "))
    sensor_points.append([x,y])

#Finding result
minimum_distance = find_best_hub_location(sensor_points)

#displaying output
print("\nMinimum total distance from hub to all sensors:")
print(round(minimum_distance, 5))

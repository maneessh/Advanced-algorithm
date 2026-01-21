import math

#calculating the total distance from the hub (x,y) to all the sensor point

def calculate_total_distance(hub_x, hub_y , sensor_point):
    total_dist = 0

    for sensor_x,sensor_y in sensor_point:
        distance = math.sqrt((hub_x - sensor_x) ** 2 +
                             (hub_y - sensor_y) ** 2)
        total_dist += distance
    return total_dist

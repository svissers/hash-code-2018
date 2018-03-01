def manhattan(loc1,loc2):
    return abs(loc1[0]-loc2[0])+abs(loc1[1]-loc2[1])

def get_ride(vehicle, ride_list, current_time):
    #ride list is sorted based on starting times
    #check if you can get at a starting coord on time
    if ride_list == []:
        return None
    distances = {}

    for ride in ride_list:
        distance_to_start = manhattan(vehicle.location, ride.start_loc)
        distances[ride] = distance_to_start
        if current_time + distance_to_start == ride.start_earliest:
            return ride
            # return min(distances, key=distances.get)
    # print ride_list
    # print distances
    return min(distances, key=distances.get)


def get_vehicle(ride, vehicle_list, current_time):
    distances = {}
    min_distance = manhattan(vehicle_list[0].location, ride.start_loc)
    min_distance_vehicle = vehicle_list[0]

    for vehicle in vehicle_list:
        distance = manhattan(vehicle.location, ride.start_loc)
        distances[vehicle] = distance

        #check if the vehicle can arrive on time, if so, prefer this one, bonus points
        if current_time + distance <= ride.start_earliest:
            pass

        if distance < min_distance:
            min_distance = distance
            min_distance_vehicle = vehicle

    return min_distance_vehicle


def assign_rides(almost_free_vehicles, ride_list, current_time):
    eligible_rides = []

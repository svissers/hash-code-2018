def manhattan(loc1,loc2):
    return abs(loc1[0]-loc2[0])+abs(loc1[1]-loc2[1])

def get_ride(vehicle, ride_list, current_time):
    #ride list is sorted based on starting times
    #check if you can get at a starting coord on time
    if ride_list == []:
        return None
    distances = {}
    rides_on_time = {}
    rides_on_time_distance_to_travel = {}
    rides_on_time_euclid = {}
    for ride in ride_list:
        distance_to_start = manhattan(vehicle.location, ride.start_loc)
        distances[ride] = distance_to_start
        if current_time + distance_to_start <= ride.start_earliest:
            rides_on_time[ride] = distance_to_start
            # rides_on_time_distance_to_travel[ride] = manhattan(ride.start_loc, ride.end_loc)
            # rides_on_time_euclid[ride] = (manhattan(ride.start_loc, ride.end_loc)**2 + distance_to_start**2)**0.5
            # return min(distances, key=distances.get)
    # print ride_list
    # print distances
    if rides_on_time != {}:
        return min(rides_on_time, key=rides_on_time.get)
    return min(distances, key=distances.get)
    # return min(distances, key=distances.get)


def get_vehicle(ride, vehicle_list, current_time):
    distances = {}
    min_distance = manhattan(vehicle_list[0].location, ride.start_loc)
    min_distance_vehicle = vehicle_list[0]

    for vehicle in vehicle_list:
        distance = manhattan(vehicle.location, ride.start_loc)
        distances[vehicle] = distance

        #check if the vehicle can arrive on time, if so, prefer this one, for bonus points
        if current_time + distance <= ride.start_earliest:
            pass

        if distance < min_distance:
            min_distance = distance
            min_distance_vehicle = vehicle

    return min_distance_vehicle


def assign_rides(almost_free_vehicles, ride_list, current_time):
    eligible_rides = []

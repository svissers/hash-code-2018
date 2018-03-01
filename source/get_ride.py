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


def assign_rides(almost_free_vehicles, ride_list, current_time):
    eligible_rides = []


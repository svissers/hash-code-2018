import sys
import get_ride

class Simulation:
    def __init__(self, rows, cols, num_vehicles, num_rides, bonus, steps):
        self.rows = int(rows)
        self.cols = int(cols)
        self.num_vehicles = int(num_vehicles)
        self.num_rides = int(num_rides)
        self.bonus = int(bonus)
        self.steps = int(steps)

        self.vehicles = [Vehicle() for i in range(num_vehicles)]
        self.rides = []


    def addRide(self, ride):
        self.rides.append(ride)


    def sortRides(self):
        self.rides = sorted(self.rides, key=lambda r: r.start_earliest)


    def run(self):
        for vehicle in self.vehicles:
            if vehicle.location == vehicle.destination:
                # get new ride for vehicle
                ride = get_ride.get_ride(vehicle, self.rides, self.current_time)
                vehicle.add_ride(ride)
                self.rides.remove(ride)

            # update state
            if vehicle.location[0] < vehicle.destination[0]:
                vehicle.location[0] += 1
            elif vehicle.location[0] > vehicle.destination[0]:
                vehicle.location[0] -= 1
            elif vehicle.location[1] < vehicle.destination[1]:
                vehicle.location[1] += 1
            elif vehicle.location[1] > vehicle.destination[1]:
                vehicle.location[1] -= 1
            else:
                pass # don't move, you're at your destination still and you didn't get a new ride.


class Ride:
    def __init__(self, start_loc, end_loc, start_earliest, finish_latest):
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.start_earliest = start_earliest
        self.finish_latest = finish_latest


class Vehicle:
    def __init__(self, location = (0, 0)):
        self.location = location
        self.destination = location
        self.rides = []

    def add_ride(ride):
        self.rides.append(ride)


def build_simulation(fn):
    f = open(fn, "r")

    lines = f.read().splitlines()

    simdata = lines[0].split(" ")
    simulation = Simulation(int(simdata[0]), int(simdata[1]), int(simdata[2]), int(simdata[3]), int(simdata[4]), int(simdata[5]))
    for line in lines[1:]:
        lineitems = line.split(" ")
        simulation.addRide(Ride((int(lineitems[0]), int(lineitems[1])), (int(lineitems[2]), int(lineitems[3])), int(lineitems[4]), int(lineitems[5])))

    f.close()

    return simulation


def main():
    sim = build_simulation(sys.argv[1])
    sim.sortRides()


if __name__ == "__main__":
    main()

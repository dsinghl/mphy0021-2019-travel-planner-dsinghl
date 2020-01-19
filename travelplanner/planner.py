import math
import numpy as np
import matplotlib.pyplot as plt
import csv


class Route:
    def __init__(self, route_filename, speed=10):
        self.__check_valid_speed(speed)
        self.speed = speed

        self.route = self.__read_route_csv(route_filename)
        self.__check_valid_route()

    def __read_route_csv(self, route_filename):
        self.__check_route_csv_format(route_filename)
        route_from_csv = []
        with open(route_filename) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=",")
            for row in read_csv:
                x_position = int(row[0])
                y_position = int(row[1])
                stop = row[2]
                step = (x_position, y_position, stop)
                route_from_csv.append(step)
        return route_from_csv

    def __check_route_csv_format(self, route_filename):
        commas_per_line = 2
        with open(route_filename) as csv_file:
            for line in csv_file:
                if line.count(",") != commas_per_line:
                    raise SyntaxError("Please check route file follows correct format.")

    def __check_valid_route(self):
        chain_code = self.generate_cc()[1]
        for digit in chain_code:
            if int(digit) % 2 != 0:
                raise ValueError(
                    "Invalid route. Bus can only travel horizontally or vertically per step."
                )

    def __check_valid_speed(self, speed):
        if speed <= 0:
            raise ValueError(
                "Bus cannot move at less than or equal to 0 minutes per step."
            )

    def __str__(self):
        return f"Route from {self.route[0][:2]} to {self.route[-1][:2]} with speed {self.speed} minutes per step"

    def __repr__(self):
        return f"route(start={self.route[0][:2]}, end={self.route[-1][:2]}, speed={self.speed})"

    def _stop_locations(self):
        stop_list = [
            (np.asarray(location), stop) for *location, stop in self.route if stop
        ]
        return stop_list

    def timetable(self):
        """Generates a timetable for a route as minutes from its first stop. """
        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += self.speed
        return stops

    def plot_map(self,):
        max_x = max([n[0] for n in self.route]) + 5  # adds padding
        max_y = max([n[1] for n in self.route]) + 5
        grid = np.zeros((max_y, max_x))
        for x, y, stop in self.route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect("equal", "datalim")
        return fig, ax

    def generate_cc(self):
        r"""
        Converts route information into a Freeman chain code
         3   2   1
          \  |  /
        4  - C -  0
          /  |  \
         5   6   7
        """
        start = self.route[0][:2]
        cc = []
        freeman_cc2cord = {
            0: (1, 0),
            1: (1, 1),
            2: (0, 1),
            3: (-1, 1),
            4: (-1, 0),
            5: (-1, -1),
            6: (0, -1),
            7: (1, -1),
        }
        freeman_coord2cc = {val: key for key, val in freeman_cc2cord.items()}
        for b, a in zip(self.route[1:], self.route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(str(freeman_coord2cc[(x_step, y_step)]))
        return start, "".join(cc)


class Passenger:

    r"""
    >>> Passenger(start=(1,1),end=(5,1), speed=20)
    passenger1((1, 1),(5, 1),20)
    """

    __lastID = 1

    def __init__(self, *, start, end, speed):
        self.__check_valid_passenger(start, end, speed)
        self.start = start
        self.end = end
        self.speed = speed
        self.id = Passenger.__lastID
        Passenger.__lastID += 1

    def __check_valid_passenger(self, start, end, speed):
        validstart = type(start) == tuple and len(start) == 2
        validend = type(end) == tuple and len(end) == 2
        validspeed = type(speed) == float or int
        valid_init = validstart and validend and validspeed
        if not valid_init:
            raise TypeError(
                "Please supply tuple of 2 values for start and end positions, and a float or integer for speed"
            )

    def __str__(self):
        return f"Start point : {self.start} \nEnd point: {self.end} \nSpeed : {self.speed} "

    def __repr__(self):
        return f"passenger{self.id}({self.start},{self.end},{self.speed})"

    def walk_distance(self):
        endpoint = np.asarray(self.end)
        startpoint = np.asarray(self.start)
        distance = np.linalg.norm(endpoint - startpoint)
        return distance

    def walk_time(self):
        distance = self.walk_distance()
        time = distance * self.speed
        return time


class Journey:
    def __init__(self, passengers, route):
        self.__valid_arguments(passengers, route)
        self.passengers = passengers
        self.route = route
        self.total_passengers = len(passengers)

    def __valid_arguments(self, passengers, route):
        validroute = isinstance(route, Route)
        valid_passenger_list = all(
            isinstance(element, Passenger) for element in passengers
        )
        valid_init = validroute and valid_passenger_list
        if not valid_init:
            raise TypeError(
                "Only route and passenger objects are allowed to create journey."
            )

    def _route(self):
        return self.route.route

    def __find_closest_stop(self, position):
        stop_locations = self.route._stop_locations()
        position = np.asarray(position)

        distances = []
        for location, stop in stop_locations:
            distance = np.linalg.norm(location - position)
            distances.append((distance, stop))

        closest_stop = min(distances)
        closest_stops = [stop for stop in distances if stop[0] == closest_stop[0]]

        if len(closest_stops) == 1:
            return closest_stops[0]
        return closest_stops

    def __pick_stop(self, stops, bus_location):
        valid_location = {"start", "end"}
        if bus_location not in valid_location:
            raise ValueError(f"Bus location must be one of {valid_location}")

        bus_times = self.route.timetable()
        stop_times = [(bus_times[stop[1]], (stop[0], stop[1])) for stop in stops]

        if bus_location == "start":
            start_stop = max(stop_times)
            return start_stop[1]
        elif bus_location == "end":
            end_stop = min(stop_times)
            return end_stop[1]

    def passenger_trip(self, passenger):

        closer_start = self.__find_closest_stop(passenger.start)
        closer_end = self.__find_closest_stop(passenger.end)

        if isinstance(closer_start, list):
            closer_start = self.__pick_stop(closer_start, "start")
        if isinstance(closer_end, list):
            closer_end = self.__pick_stop(closer_end, "end")

        return (closer_start, closer_end)

    def _passenger_trip_time(self, passenger):
        (walk_dist_start, start_stop), (walk_dist_end, end_stop) = self.passenger_trip(
            passenger
        )
        bus_times = self.route.timetable()

        bus_travel = bus_times[end_stop] - bus_times[start_stop]
        walk_travel = (
            walk_dist_start * passenger.speed + walk_dist_end * passenger.speed
        )
        bus_walk_travel = bus_travel + walk_travel

        walking_only = passenger.walk_time()

        same_start_end_stop = start_stop == end_stop
        end_stop_before_start_stop = bus_times[end_stop] < bus_times[start_stop]
        walking_faster_than_bus = walking_only < bus_walk_travel

        walking = (
            same_start_end_stop or end_stop_before_start_stop or walking_faster_than_bus
        )

        if walking:
            travel_time = {"walk": walking_only, "bus": 0}
        else:
            travel_time = {"walk": walk_travel, "bus": bus_travel}

        return travel_time

    def travel_time(self, passenger_id):
        for passenger in self.passengers:
            if passenger_id == passenger.id:
                return self._passenger_trip_time(passenger)
        return ValueError(f"A passenger with Id={passenger_id} does not exist.")

    def print_time_stats(self):
        walk_total = 0
        bus_total = 0
        for passenger in self.passengers:
            time = self.travel_time(passenger.id)
            walk_total += time["walk"]
            bus_total += time["bus"]
        av_bus_time = bus_total / self.total_passengers
        av_walk_time = walk_total / self.total_passengers

        print(f"Average time on bus: {av_bus_time:.0f} min")
        print(f"Average walking time: {av_walk_time:.0f} min")

    def plot_bus_load(self,):
        stops = {step[2]: 0 for step in self._route() if step[2]}
        print(stops)
        for passenger in self.passengers:
            travel_time = self.travel_time(passenger.id)
            if travel_time["bus"] != 0:
                trip = self.passenger_trip(passenger)
                stops[trip[0][1]] += 1
                stops[trip[1][1]] -= 1
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        print(stops)
        fig, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where="post")
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        return fig, ax


def read_passengers(passenger_filename):
    __check_passenger_csv_format(passenger_filename)
    passengers = []
    with open(passenger_filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=",")
        for row in read_csv:
            start = (float(row[0]), float(row[1]))
            end = (float(row[2]), float(row[3]))
            speed = float(row[4])
            passenger = (start, end, speed)
            passengers.append(passenger)
    return passengers


def __check_passenger_csv_format(passenger_filename):
    commas_per_line = 4
    with open(passenger_filename) as csv_file:
        for line in csv_file:
            if line.count(",") != commas_per_line:
                raise IndexError("Please check passenger file follows correct format.")

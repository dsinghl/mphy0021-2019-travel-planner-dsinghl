import math
import numpy as np
import matplotlib.pyplot as plt
import csv


class Route:
    def __init__(self, route_filename):
        route_from_csv = []
        with open(route_filename) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=",")
            for row in read_csv:
                x_position = int(row[0])
                y_position = int(row[1])
                stop = row[2]
                step = (x_position, y_position, stop)
                route_from_csv.append(step)
        self.route = route_from_csv

    def timetable(self):
        """Generates a timetable for a route as minutes from its first stop. """
        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += 10
        return stops

    def plot_map(self):
        max_x = max([n[0] for n in self.route]) + 5  # adds padding
        max_y = max([n[1] for n in self.route]) + 5
        grid = np.zeros((max_y, max_x))
        for x, y, stop in self.route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        _, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect("equal", "datalim")
        plt.show()

    def generate_cc(self):
        """
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
            3: (-1, 0),
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

    id_list = [0]

    def __init__(self, *, start, end, speed):
        validstart = type(start) == tuple and len(start) == 2
        validend = type(end) == tuple and len(end) == 2
        validspeed = type(speed) == float or int
        valid_init = validstart and validend and validspeed
        if valid_init:
            self.start = start
            self.end = end
            self.speed = speed
        else:
            raise TypeError(
                "Please supply tuple of 2 values for start and end, and a float or integer for speed"
            )
        self.id = self.id_list[-1] + 1
        self.id_list.append(self.id)

    def __str__(self):
        return f"Start point : {self.start} \nEnd point: {self.end} \nSpeed : {self.speed} "

    def __repr__(self):
        return f"PassengerId({self.id})"

    def walk_time(self):
        endpoint = np.asarray(self.end)
        startpoint = np.asarray(self.start)
        distance = np.linalg.norm(endpoint - startpoint)
        time = distance * self.speed
        return time


class Journey:
    def __init__(self, route, passengers):
        validroute = isinstance(route, Route)
        valid_passenger_list = all(
            isinstance(element, Passenger) for element in passengers
        )
        valid_init = validroute and valid_passenger_list
        if valid_init:
            self.passengers = passengers
            self.route = route
        else:
            raise TypeError(
                "must use route and passenger objects to initialise journey"
            )

    def _route(self):
        return self.route.route

    def passenger_trip(self, passenger):
        stops = [step for step in self._route() if step[2]]  # calculate closer stops
        ## to start
        distances = [
            (
                math.sqrt(
                    (x - passenger.start[0]) ** 2 + (y - passenger.start[1]) ** 2
                ),
                stop,
            )
            for x, y, stop in stops
        ]
        closer_start = min(distances)
        print(distances)
        ## to end
        distances = [
            (math.sqrt((x - passenger.end[0]) ** 2 + (y - passenger.end[1]) ** 2), stop)
            for x, y, stop in stops
        ]
        closer_end = min(distances)

        stop_pos = {v[2]: i for i, v in enumerate(stops)}
        start_pos = stop_pos[closer_start[1]]
        end_pos = stop_pos[closer_end[1]]
        if start_pos >= end_pos:
            closer_start = closer_end
        return (closer_start, closer_end)

    def passenger_trip_time(self, passenger):
        walk_distance_stops = self.passenger_trip(passenger)
        bus_times = self.route.timetable()
        bus_travel = (
            bus_times[walk_distance_stops[1][1]] - bus_times[walk_distance_stops[0][1]]
        )
        walk_travel = (
            walk_distance_stops[0][0] * passenger.speed
            + walk_distance_stops[1][0] * passenger.speed
        )
        return bus_travel + walk_travel

    def plot_bus_load(self):
        stops = {step[2]: 0 for step in self._route() if step[2]}
        print(stops)
        for passenger in passengers:
            trip = self.passenger_trip(passenger)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        print(stops)
        _, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where="post")
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        plt.show()

    def map(self):
        _, ax = plt.subplots()

        for passen in passengers:
            x = [passen.start[0], passen.end[0]]
            y = [passen.start[1], passen.end[1]]
            for _ in range(2):
                ax.scatter(x[0], y[0], color="green")
                ax.scatter(x[1], y[1], color="red")
            ax.plot(x, y, linestyle="--", color="blue")

        for x_route, y_route, stop in self._route():
            if stop:
                ax.scatter(x_route, y_route, s=75, marker="s")
                ax.text(
                    x_route,
                    y_route,
                    stop,
                    bbox=dict(facecolor="white", edgecolor="black", pad=0.1),
                )

        route_step_x = [step[0] for step in self._route()]
        route_step_y = [step[1] for step in self._route()]
        ax.plot(route_step_x, route_step_y, linewidth=10.0, alpha=0.5)

        ax.set_aspect("equal")
        plt.show()


def read_passengers(passenger_filename):
    passengers = []
    with open(passenger_filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=",")
        for row in read_csv:
            start = (int(row[0]), int(row[1]))
            end = (int(row[2]), int(row[3]))
            speed = int(row[4])
            passenger = (start, end, speed)
            passengers.append(passenger)
    return passengers


if __name__ == "__main__":
    test = Route("route.csv")
    print(test.route)
    passengers = [
        Passenger(start=start, end=end, speed=speed)
        for start, end, speed in read_passengers("passengers.csv")
    ]
    print(passengers)
    j = Journey(test, passengers)
    a = j._route()
    j.map()
    j.plot_bus_load()
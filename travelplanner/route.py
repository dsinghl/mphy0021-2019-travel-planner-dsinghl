import numpy as np
import matplotlib.pyplot as plt
import csv


class Route:

    """
    Base class for a bus route.

    Parameters:
        route_filename : str
            The file location of the route file.
            A csv file is expected, each line with x_pos,y_pos,stop.
            Each line must be one step
        speed: int or float, optional
            Specifies the speed of the bus in minutes per step

    Attributes:
        route: list of tuple
            A list specifying position, and stop (if exists) of each bus step.
        speed: int or float
            Number of minutes per step

    Raises:
        ValueError:
            If the csv file is formatted incorrectly.
            If the bus moves diagonally in a step.
            If the bus moves more than one unit per step.
    """

    def __init__(self, route_filename, speed=10):
        self.__check_valid_speed(speed)
        self.speed = speed

        self.route = self.__read_route_csv(route_filename)
        self.__check_valid_route()

    def __read_route_csv(self, route_filename):
        route_from_csv = []
        with open(route_filename) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=",")
            for row in read_csv:
                step = self.__parse_csv_line(row)
                route_from_csv.append(step)
        return route_from_csv

    def __parse_csv_line(self, row):
        rowlen = len(row)
        while True:
            try:
                rowlen == 3
                x_position = int(row[0])
                y_position = int(row[1])
                stop = row[2]
            except BaseException:
                break
            return (x_position, y_position, stop)
        raise ValueError("Please check route file follows correct format.")

    def __check_valid_route(self):
        chain_code = self.generate_cc()[1]
        for digit in chain_code:
            invalid_cc = int(digit) % 2 != 0
            if invalid_cc:
                raise ValueError(
                    "Bus cannot travel diagonally."
                )

    def __check_valid_speed(self, speed):
        if speed <= 0:
            raise ValueError(
                "Bus cannot move at less than or equal to 0 minutes per step."
            )

    def __str__(self):
        return f"route({self.route[0][:2]},{self.route[-1][:2]},{self.speed})"

    def __repr__(self):
        return f"route({self.route[0][:2]},{self.route[-1][:2]},{self.speed})"

    def _stop_locations(self):
        stop_list = [
            (np.asarray(location), stop)
            for *location, stop in self.route if stop
        ]
        return stop_list

    def timetable(self):
        """
        Generates a timetable for a route as minutes from its first stop.

        Returns:
            timetable: dict of str: int or float
                A dicionary of stops and time taken by bus to reach stop.
        """

        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += self.speed
        return stops

    def plot_map(self):
        """Method to visualise bus route on a map.

        Returns:
            fig: matplotlib.figure
            ax: matplotlib.axes
        """

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


        Raises:
            ValueError:
                If the bus moves more than one unit in any of the directions.

        Returns:
            start: tuple
                Starting coordinate of bus route
            chain_code: string
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
            try:
                cc.append(str(freeman_coord2cc[(x_step, y_step)]))
            except BaseException:
                raise ValueError("Bus can only move one unit at a time")
        return start, "".join(cc)

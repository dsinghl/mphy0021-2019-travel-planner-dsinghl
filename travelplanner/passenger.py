import numpy as np
import csv


def read_passengers(passenger_filename):
    __check_passenger_csv_format(passenger_filename)
    passengers = []
    with open(passenger_filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=",")
        for row in read_csv:
            passenger = __parse_csv_line(row)
            passengers.append(passenger)
    return passengers


def __check_passenger_csv_format(passenger_filename):
    commas_per_line = 4
    with open(passenger_filename) as csv_file:
        for line in csv_file:
            if line.count(",") != commas_per_line:
                raise IndexError(
                    "Please check passenger file follows correct format.")


def __parse_csv_line(row):
    rowlen = len(row)
    while True:
        try:
            rowlen == 5
            start = (float(row[0]), float(row[1]))
            end = (float(row[2]), float(row[3]))
            speed = float(row[4])
        except BaseException:
            break
        return (start, end, speed)
    raise ValueError("Please check passenger file follows correct format.")


class Passenger:

    r"""
      Base class for a passenger.

    Parameters:
        **start : (int or float, int or float)
            Start position of passenger trip.
        **end: (int or float, int or float)
            End position of passenger trip.
        **speed: int or float
            walking speed of passenger in min/step.

    Attributes:
        start : (int or float, int or float)
            Start position of passenger trip.
        end: (int or float, int or float)
            End position of passenger trip.
        speed: int or float
            walking speed of passenger in min/step.
        id: int
            Unique Id of passenger

    Raises:
        TypeError:
            If correct parameters are not provided

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
        validstart = isinstance(start, tuple) and len(start) == 2
        validend = isinstance(end, tuple) and len(end) == 2
        validspeed = isinstance(speed, float) or int
        valid_init = validstart and validend and validspeed
        if not valid_init:
            raise TypeError(
                "Please supply tuple of 2 values for start and end positions, "
                "and a float or integer for speed"
            )

    def __str__(self):
        return f"passenger{self.id}({self.start},{self.end},{self.speed})"

    def __repr__(self):
        return f"passenger{self.id}({self.start},{self.end},{self.speed})"

    def walk_distance(self):
        """
        Returns:
            distance: float
                Distance passenger must walk if not using bus.
        """
        endpoint = np.asarray(self.end)
        startpoint = np.asarray(self.start)
        distance = np.linalg.norm(endpoint - startpoint)
        return distance

    def walk_time(self):
        """
        Returns:
            time: float
                Walk time if passenger does not use bus.
        """
        distance = self.walk_distance()
        time = distance * self.speed
        return time

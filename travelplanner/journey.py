import numpy as np
import matplotlib.pyplot as plt
from travelplanner.route import Route
from travelplanner.passenger import Passenger


class Journey:

    """
    Journey class for passengers and bus routes.

    Parameters:
        passengers: list of travelplanner Passenger objects
            List of passenger objects that will be taking the bus
        route: travelplanner Route object
            Bus route for passengers

    Attributes:
        passengers: list of travelplanner Passenger objects
            List of passenger objects that will be taking the bus
        route: travelplanner Route object
            Bus route for passengers
        total_passengers: int
            Total number of passengers

    Raises:
        TypeError:
            Only takes travelplanner objects

    """

    def __valid_arguments(self, passengers, route):
        validroute = isinstance(route, Route)
        valid_passenger_list = all(
            isinstance(element, Passenger) for element in passengers
        )
        valid_init = validroute and valid_passenger_list
        if not valid_init:
            raise TypeError("Only route and passenger objects allowed.")

    def __init__(self, passengers, route):
        self.__valid_arguments(passengers, route)
        self.passengers = passengers
        self.route = route
        self.total_passengers = len(passengers)

    def __str__(self):
        return f"journey({self.route}, num_passengers:{self.total_passengers})"

    def __repr__(self):
        return f"journey({self.route}, num_passengers:{self.total_passengers})"

    def _route(self):
        return self.route.route

    def _find_closest_stop(self, position):
        stop_locations = self.route._stop_locations()
        position = np.asarray(position)

        distances = []
        for location, stop in stop_locations:
            distance = np.linalg.norm(location - position)
            distances.append((distance, stop))

        closest_stop = min(distances)
        closest_stops = [stop for stop in distances
                         if stop[0] == closest_stop[0]]

        if len(closest_stops) == 1:
            return closest_stops[0]
        return closest_stops

    def _pick_stop(self, stops, bus_location):
        bus_times = self.route.timetable()
        stop_times = [(bus_times[stop[1]], (stop[0], stop[1]))
                      for stop in stops]

        if bus_location == "start":
            start_stop = max(stop_times)
            return start_stop[1]
        elif bus_location == "end":
            end_stop = min(stop_times)
            return end_stop[1]

    def _passenger_trip_time(self, passenger):
        closer_start, closer_end = self.passenger_trip(passenger)

        bus_times = self.route.timetable()
        bus_travel = bus_times[closer_end[1]] - bus_times[closer_start[1]]
        walk_travel = (
            closer_start[0] * passenger.speed + closer_end[0] * passenger.speed
        )
        walking_only = passenger.walk_time()

        walking = closer_start[1] == closer_end[1]

        if walking:
            travel_time = {"walk": walking_only, "bus": 0}
        else:
            travel_time = {"walk": walk_travel, "bus": bus_travel}

        return travel_time

    def passenger_trip(self, passenger):
        """
        Used to calculate closest bus stops for passenger.
        Picks the stops which minimise walk time and minimise bus time.

        Arguments:
            passenger: travelplanner Passenger object
                Passengers for which stops are calculated

        Returns:
            closer_start: (float, str)
                Walking distance from start to start stop, stop name.

            closer_end: (float, str)
                Walking distance from end stop to end, stop name.
        """

        closer_start = self._find_closest_stop(passenger.start)
        closer_end = self._find_closest_stop(passenger.end)

        if isinstance(closer_start, list):
            closer_start = self._pick_stop(closer_start, "start")
        if isinstance(closer_end, list):
            closer_end = self._pick_stop(closer_end, "end")

        bus_times = self.route.timetable()
        bus_travel = bus_times[closer_end[1]] - bus_times[closer_start[1]]
        if bus_travel <= 0:
            closer_end = closer_start

        return (closer_start, closer_end)

    def travel_time(self, passenger_id):
        """
        Gives total travel time of passenger

        Arguments:
            passenger_id: int
                Id of passenger whose travel time is required.

        Returns:
            travel_time: {str: float}
                Returns the total walk and bus time as a dictionary

        """
        for passenger in self.passengers:
            if passenger_id == passenger.id:
                return self._passenger_trip_time(passenger)
        return ValueError(
            f"A passenger with Id={passenger_id} does not exist.")

    def print_time_stats(self):
        """
        Prints total average walk and bus time for all passengers on trip.
        """
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

    def plot_bus_load(self):
        """
        Returns a matplotlib object for a plot of passengers on bus vs stop
        """
        stops = {key: 0 for key, _ in self.route.timetable().items()}
        for passenger in self.passengers:
            trip = self.passenger_trip(passenger)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
        prev = None
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        fig, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where="post")
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        return fig, ax

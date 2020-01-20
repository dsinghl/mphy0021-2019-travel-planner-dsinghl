"""
Travelplanner command line interface

Mandatory:
    route_file
    passengers_file
        These must be csv files

Optional:
    --speed int or float
        Supply and value for minutes per step of bus
    --saveplots
        Flag, saves bus load and map plots to map.png and load.png

"""
from travelplanner.route import Route
from travelplanner.passenger import Passenger, read_passengers
from travelplanner.journey import Journey
import matplotlib.pyplot as plt
from argparse import ArgumentParser as arg


def main():

    parser = arg(
        description=(
            "Travelplanner command line inferface. "
            "Used to calculate journeys for passengers on a bus route."))
    parser.add_argument(
        "route_file",
        type=str,
        help=(
            'Route csv file name, for example "route.csv".'
            "Use path if file not in current dirrectory."
        ),
    )
    parser.add_argument(
        "passenger_file",
        type=str,
        help=(
            'Passengers csv file name, for example "passengers.csv". '
            "Use path if file not in current dirrectory."
        ),
    )
    parser.add_argument(
        "--speed",
        default=10,
        type=float,
        help="Accepts number indicating minutes per step.",
    )
    parser.add_argument(
        "--saveplots",
        action="store_true",
        help=(
            "(OPTIONAL) Saves two plots of bus "
            "load and route in current directory."
        ),
    )

    arguments = parser.parse_args()
    args = vars(arguments)
    passengers = [
        Passenger(start=start, end=end, speed=speed)
        for start, end, speed in read_passengers(args["passenger_file"])
    ]
    route = Route(args["route_file"], speed=args["speed"])
    journey = Journey(passengers, route)

    print(" Stops: minu tes from start\n", journey.route.timetable())
    for passenger in passengers:
        print(f"Trip for passenger: {passenger.id}")
        start, end = journey.passenger_trip(passenger)
        travel_time = journey.travel_time(passenger.id)
        walk_time = travel_time["walk"]
        bus_time = travel_time["bus"]
        total_time = walk_time + bus_time
        if bus_time == 0:
            walk_distance = passenger.walk_distance()
            print(
                (
                    f" No bus route quicker than walking.\n"
                    f"Walk {walk_distance:3.2f} units to your destination."
                )
            )
        else:
            print(
                (
                    f" Walk {start[0]:3.2f} units to stop {start[1]}, \n"
                    f" get on the bus and alite at stop {end[1]} and \n"
                    f" walk {end[0]:3.2f} units to your destination."
                )
            )
        print(f"Total time of travel: {total_time:03.2f} minutes")

    if args["saveplots"]:
        plt.figure()

        journey.route.plot_map()
        plt.savefig("./map.png")
        plt.close()

        journey.plot_bus_load()
        plt.savefig("./load.png")
        plt.close()


if __name__ == "__main__":
    main()

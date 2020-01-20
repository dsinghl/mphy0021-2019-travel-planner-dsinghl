import pytest
import os
from travelplanner.route import Route
from travelplanner.passenger import Passenger, read_passengers
from travelplanner.journey import Journey
import yaml


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "tests_data")

fixtures_file = os.path.join(THIS_DIR, "fixtures.yml")
with open(fixtures_file, "r") as yamlfile:
    fixtures = yaml.safe_load(yamlfile)


def get_path(filename):
    return os.path.join(DATA_DIR, filename)


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("route_constructor_fail_tests"),
    ids=["csv_format_fail", "bus_neg_speed_fail", "diagonal_route_fail"],
)
def test_fail_route_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties["test_input"].values())
    expected = properties["expected"]
    file = get_path(test_input[0])
    speed = test_input[1]
    with pytest.raises(Exception, match=expected):
        Route(file, speed=speed)


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("route_constructor_pass_tests"),
    ids=["csv_format_pass"])
def test_pass_route_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties["test_input"].values())
    expected = list(properties["expected"].values())
    expected_route = [tuple(i) for i in expected[0]]
    expected_speed = expected[1]
    expected_repr = expected[2]
    expected_str = expected[3]
    file = get_path(test_input[0])
    speed = test_input[1]
    route = Route(file, speed=speed)
    assert route.route == expected_route
    assert route.speed == expected_speed
    assert repr(route) == expected_repr
    assert str(route) == expected_str


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("route_timetable_tests"),
    ids=["unspecified_speed", "specified_speed"],
)
def test_timetable(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties["test_input"].values())
    filename = get_path(test_input[0])
    expected = properties["expected"]
    if len(test_input) > 1:
        speed = test_input[1]
        route = Route(filename, speed=speed)
    else:
        route = Route(filename)
    assert route.timetable() == expected


@pytest.mark.parametrize(
    "test_name", fixtures.get("route_generate_cc_tests"), ids=["pass"]
)
def test_generate_cc(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties["test_input"].values())
    filename = get_path(test_input[0])
    route = Route(filename,)
    expected_dict = properties["expected"]
    expected = (tuple(expected_dict['start']), expected_dict['cc'])
    print(type(expected))
    assert expected == route.generate_cc()


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("passenger_constructor_tests"),
    ids=["incorrect_args"])
def test__fail_passenger_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties["test_input"].values())
    expected = properties["expected"]
    start, end, speed = test_input[0], test_input[1], test_input[2]
    with pytest.raises(Exception, match=expected):
        Passenger(start=start, end=end, speed=speed)


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("read_passenger_fail_tests"),
    ids=["csv_format_fail"])
def test_read_passengers(test_name):
    properties = list(test_name.values())[0]
    test_input = properties["test_input"]
    expected = properties["expected"]
    file = get_path(test_input)
    with pytest.raises(Exception, match=expected):
        read_passengers(file)


def test_walk_time():
    passenger = Passenger(start=(0, 0), end=(0, 5), speed=20)
    expected = 5 * 20
    assert passenger.walk_time() == expected


@pytest.fixture(scope="session")
def route():
    route_file = get_path("test_route_special_cases.csv")
    route = Route(route_file)
    return route


@pytest.fixture(scope="session")
def passengers():
    passengers_file = get_path("test_passengers_special_cases.csv")
    passengers = [
        Passenger(start=start, end=end, speed=speed)
        for start, end, speed in read_passengers(passengers_file)
    ]
    return passengers


@pytest.fixture(scope="session")
def journey(passengers, route):
    journey = Journey(passengers, route)
    return journey


@pytest.mark.parametrize(
    "test_name",
    fixtures.get("journey_travel_time"),
    ids=["same_distance_from_two_stops", "only_walk"],
)
def test_travel_time(test_name, journey):
    properties = list(test_name.values())[0]
    test_input = properties["test_input"]
    test_input = journey.passengers[test_input].id
    expected = properties["expected"]
    assert journey.travel_time(test_input) == expected


def test_journey_constructor_fail(route, passengers):
    route_bad = [1, 2, "A", 3, 4, "", 5, 6, "C"]
    passenger_bad = [(1, 1), (5, 1), 20]
    message = "Only route and passenger objects allowed."
    with pytest.raises(TypeError, match=message):
        Journey(passenger_bad, route)
    with pytest.raises(TypeError, match=message):
        Journey(passengers, route_bad)


def test_print_time_stats(capsys, journey):
    print("Average time on bus: 17 min")
    print("Average walking time: 198 min")
    out_exp, _ = capsys.readouterr()
    journey.print_time_stats()
    out_test, _ = capsys.readouterr()
    assert out_test == out_exp


def test_journey_constructor_pass(journey, route, passengers):
    expected = (f"journey({repr(route)}," +
                f" num_passengers:{journey.total_passengers})")
    assert repr(journey) == expected
    assert str(journey) == expected

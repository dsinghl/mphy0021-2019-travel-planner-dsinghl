import pytest
import os
from .. import planner as pl
import yaml
import numpy as np


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, 'tests_data')

fixtures_file = os.path.join(THIS_DIR, 'fixtures.yml')
with open(fixtures_file, 'r') as yamlfile:
    fixtures = yaml.safe_load(yamlfile)


def get_path(filename):
    return os.path.join(DATA_DIR, filename)


@pytest.mark.parametrize('test_name', fixtures.get('route_constructor_fail_tests'),ids=['csv_format_fail', 'bus_neg_speed_fail', 'diagonal_route_fail'])
def test_fail_route_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties['test_input'].values())
    expected = properties['expected']
    file = get_path(test_input[0])
    speed = test_input[1]
    with pytest.raises(Exception, match=expected):
        pl.Route(file, speed=speed)

@pytest.mark.parametrize('test_name', fixtures.get('route_constructor_pass_tests'),ids=['csv_format_pass',])
def test_pass_route_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties['test_input'].values())
    expected = list(properties['expected'].values())
    expected_route = [tuple(i) for i in expected[0]]
    expected_speed = expected[1]
    expected_repr = expected[2]
    expected_str = expected[3]
    file = get_path(test_input[0])
    speed = test_input[1]
    route = pl.Route(file, speed=speed)
    assert route.route == expected_route
    assert route.speed == expected_speed
    assert repr(route) == expected_repr
    assert str(route) == expected_str

@pytest.mark.parametrize('test_name', fixtures.get('route_timetable_tests'),ids=['unspecified_speed','specified_speed'])
def test_timetable(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties['test_input'].values())
    filename = get_path(test_input[0])
    expected = properties['expected']
    if len(test_input) > 1:
        speed = test_input[1]
        route = pl.Route(filename, speed=speed)
    else:
        route = pl.Route(filename)
    assert route.timetable() == expected


@pytest.mark.parametrize('test_name', fixtures.get('passenger_constructor_tests'),ids=['incorrect_args',])
def test__fail_passenger_constructor(test_name):
    properties = list(test_name.values())[0]
    test_input = list(properties['test_input'].values())
    expected = properties['expected']
    start, end, speed = test_input[0], test_input[1], test_input[2]
    with pytest.raises(Exception, match=expected):
        pl.Passenger(start=start, end=end, speed=speed)


@pytest.mark.parametrize('test_name', fixtures.get('read_passenger_fail_tests'),ids=['csv_format_fail',])
def test_read_passengers(test_name):
    properties = list(test_name.values())[0]
    test_input = properties['test_input']
    expected = properties['expected']
    file = get_path(test_input)
    with pytest.raises(Exception, match=expected):
        pl.read_passengers(file)


@pytest.fixture(scope="module")
def journey():
    pl.Journey.__lastID = 1
    passengers_file = get_path('test_passengers_special_cases.csv')
    route_file = get_path('test_route_special_cases.csv')
    passengers = [pl.Passenger(start=start, end=end, speed=speed) for start, end, speed in pl.read_passengers(passengers_file)]
    route = pl.Route(route_file)
    journey = pl.Journey(passengers, route)
    type(journey).__lastID=1
    return journey


@pytest.mark.parametrize('test_name', fixtures.get('journey_travel_time'),ids=['same_distance_from_two_stops','only_walk'])
def test_travel_time(test_name, journey):
    properties = list(test_name.values())[0]
    test_input = properties['test_input']
    expected = properties['expected']
    print(journey.passengers)
    assert journey.travel_time(test_input) == expected


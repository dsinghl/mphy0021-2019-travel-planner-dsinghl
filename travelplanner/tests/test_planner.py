import pytest
import csv
import os
from .. import planner as pl


@pytest.fixture
def route():
    _route = [
        (2, 1, "A"),
        (3, 1, ""),
        (4, 1, ""),
        (5, 1, ""),
        (6, 1, ""),
        (7, 1, "B"),
        (7, 2, ""),
        (8, 2, ""),
        (9, 2, ""),
        (10, 2, ""),
        (11, 2, "C"),
        (11, 1, ""),
        (12, 1, ""),
        (13, 1, ""),
        (14, 1, ""),
        (14, 2, "D"),
        (14, 3, ""),
        (14, 4, ""),
        (13, 4, ""),
        (12, 4, ""),
        (11, 4, ""),
        (10, 4, ""),
        (9, 4, ""),
        (9, 5, "E"),
        (9, 6, ""),
        (10, 6, ""),
        (11, 6, "F"),
        (12, 6, ""),
        (13, 6, ""),
        (14, 6, ""),
        (15, 6, ""),
        (16, 6, "G"),
    ]
    with open("test_route.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in _route:
            writer.writerow(row)
    route = pl.Route("test_route.csv")
    os.remove("test_route.csv")

    return route


@pytest.fixture
def passengers():
    _passengers = [
        ((5, 4), (0, 17), 24),
        ((4, 1), (2, 1), 15),
        ((15, 7), (0, 22), 22),
        ((1, 11), (2, 0), 18),
    ]

    with open("test_passengers.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in _passengers:
            writer.writerow(row)
    passengers = pl.read_passengers("test_route.csv")
    os.remove("test_passengers.csv")

    return passengers


@pytest.fixture
def passenger():
    start = (5, 4)
    end = (0, 17)
    speed = 24
    passenger = pl.Passenger(start, end, speed)

    return passenger


def test_timetable(route):
    ttable = route.timetable()
    correct = {"A": 0, "B": 50, "C": 100, "D": 150, "E": 230, "F": 260, "G": 310}

    assert ttable == correct


def test_generate_cc(route):
    cc = route.generate_cc()
    correct_cc = ((2, 1), "0000020000600022244444220000000")
    print(type(cc))

    assert cc == correct_cc

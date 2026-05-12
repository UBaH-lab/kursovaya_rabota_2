import pytest

from src.aeroplane import Aeroplane


@pytest.fixture
def plane():
    return Aeroplane(
        icao24="abc123",
        callsign="UAL1621",
        origin_country="United States",
        velocity=250.5,
        geo_altitude=10000.0,
        baro_altitude=9800.0,
        on_ground=False,
    )


def test_aeroplane_init(plane):
    assert plane.icao24 == "abc123"
    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 250.5
    assert plane.geo_altitude == 10000.0


def test_invalid_velocity():
    with pytest.raises(ValueError):
        Aeroplane("abc123", "TEST", "Spain", -100, 1000, 900, False)


def test_comparison():
    plane1 = Aeroplane("1", "A", "Spain", 200, 10000, 9500, False)
    plane2 = Aeroplane("2", "B", "France", 300, 11000, 10500, False)

    assert plane2 > plane1
    assert plane1 < plane2


def test_is_faster_than():
    plane1 = Aeroplane("1", "A", "Spain", 200, 10000, 9500, False)
    plane2 = Aeroplane("2", "B", "France", 300, 11000, 10500, False)

    assert plane2.is_faster_than(plane1) is True
    assert plane1.is_faster_than(plane2) is False


def test_is_higher_than():
    plane1 = Aeroplane("1", "A", "Spain", 200, 10000, 9500, False)
    plane2 = Aeroplane("2", "B", "France", 300, 11000, 10500, False)

    assert plane2.is_higher_than(plane1) is True
    assert plane1.is_higher_than(plane2) is False


def test_to_dict(plane):
    data = plane.to_dict()
    assert data["icao24"] == "abc123"
    assert data["callsign"] == "UAL1621"


def test_from_dict():
    data = {
        "icao24": "abc123",
        "callsign": "TEST123",
        "origin_country": "Germany",
        "velocity": 220,
        "geo_altitude": 9000,
        "baro_altitude": 8800,
        "on_ground": False,
    }
    plane = Aeroplane.from_dict(data)
    assert plane.callsign == "TEST123"
    assert plane.origin_country == "Germany"

import pytest

from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes_by_country,
    get_aeroplanes_by_altitude,
    get_airborne_aeroplanes,
    get_airborne_with_positive_altitude,
    get_top_aeroplanes,
    sort_aeroplanes_by_altitude_desc,
    sort_aeroplanes_by_velocity_desc,
)


@pytest.fixture
def planes():
    return [
        Aeroplane("1", "A1", "Spain", 200, 10000, 9500, False),
        Aeroplane("2", "A2", "France", 250, 12000, 11500, False),
        Aeroplane("3", "A3", "Spain", 180, 0, 7800, True),
    ]


def test_filter_by_country(planes):
    filtered = filter_aeroplanes_by_country(planes, ["Spain"])
    assert len(filtered) == 2


def test_filter_by_altitude(planes):
    filtered = get_aeroplanes_by_altitude(planes, 9000, 13000)
    assert len(filtered) == 2


def test_filter_by_altitude_invalid(planes):
    with pytest.raises(ValueError):
        get_aeroplanes_by_altitude(planes, 13000, 9000)


def test_get_airborne_aeroplanes(planes):
    filtered = get_airborne_aeroplanes(planes)
    assert len(filtered) == 2


def test_get_airborne_with_positive_altitude(planes):
    filtered = get_airborne_with_positive_altitude(planes)
    assert len(filtered) == 2


def test_sort_by_altitude_desc(planes):
    sorted_planes = sort_aeroplanes_by_altitude_desc(planes)
    assert sorted_planes[0].geo_altitude == 12000


def test_sort_by_velocity_desc(planes):
    sorted_planes = sort_aeroplanes_by_velocity_desc(planes)
    assert sorted_planes[0].velocity == 250


def test_get_top_aeroplanes(planes):
    sorted_planes = sort_aeroplanes_by_altitude_desc(planes)
    top_planes = get_top_aeroplanes(sorted_planes, 2)
    assert len(top_planes) == 2


def test_get_top_invalid():
    with pytest.raises(ValueError):
        get_top_aeroplanes([], 0)

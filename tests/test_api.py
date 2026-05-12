import pytest
import requests

from src.api import AeroplanesAPI


class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self._json_data = json_data or {}
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_connect_success(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        return MockResponse(status_code=200)

    monkeypatch.setattr(api.session, "get", mock_get)
    assert api.connect() is True


def test_connect_fail(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Connection error")

    monkeypatch.setattr(api.session, "get", mock_get)
    assert api.connect() is False


def test_get_country_bounding_box_success(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        return MockResponse([{"boundingbox": ["10.0", "20.0", "30.0", "40.0"]}])

    monkeypatch.setattr(api.session, "get", mock_get)
    result = api.get_country_bounding_box("India")
    assert result == (10.0, 20.0, 30.0, 40.0)


def test_get_country_bounding_box_country_not_found(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        return MockResponse([])

    monkeypatch.setattr(api.session, "get", mock_get)

    with pytest.raises(ValueError, match="не найдена"):
        api.get_country_bounding_box("UnknownCountry")


def test_get_country_bounding_box_invalid_box(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        return MockResponse([{"boundingbox": ["10.0", "20.0"]}])

    monkeypatch.setattr(api.session, "get", mock_get)

    with pytest.raises(ValueError, match="Некорректные данные"):
        api.get_country_bounding_box("India")


def test_get_country_bounding_box_request_error(monkeypatch):
    api = AeroplanesAPI()

    def mock_get(*args, **kwargs):
        raise requests.RequestException("Network error")

    monkeypatch.setattr(api.session, "get", mock_get)

    with pytest.raises(ConnectionError, match="Nominatim API"):
        api.get_country_bounding_box("India")


def test_get_aeroplanes_success(monkeypatch):
    api = AeroplanesAPI()

    monkeypatch.setattr(
        api, "get_country_bounding_box", lambda country: (10.0, 20.0, 30.0, 40.0)
    )

    def mock_get(*args, **kwargs):
        return MockResponse(
            {
                "states": [
                    [
                        "abc123",
                        "TEST123 ",
                        "India",
                        111,
                        222,
                        77.1,
                        28.6,
                        10000.0,
                        False,
                        250.0,
                        180.0,
                        0.0,
                        None,
                        10500.0,
                    ]
                ]
            }
        )

    monkeypatch.setattr(api.session, "get", mock_get)

    result = api.get_aeroplanes("India")
    assert len(result) == 1
    assert result[0]["icao24"] == "abc123"
    assert result[0]["callsign"] == "TEST123"
    assert result[0]["origin_country"] == "India"
    assert result[0]["geo_altitude"] == 10500.0


def test_get_aeroplanes_empty_states(monkeypatch):
    api = AeroplanesAPI()

    monkeypatch.setattr(
        api, "get_country_bounding_box", lambda country: (10.0, 20.0, 30.0, 40.0)
    )

    def mock_get(*args, **kwargs):
        return MockResponse({"states": []})

    monkeypatch.setattr(api.session, "get", mock_get)

    result = api.get_aeroplanes("India")
    assert result == []


def test_get_aeroplanes_request_error(monkeypatch):
    api = AeroplanesAPI()

    monkeypatch.setattr(
        api, "get_country_bounding_box", lambda country: (10.0, 20.0, 30.0, 40.0)
    )

    def mock_get(*args, **kwargs):
        raise requests.RequestException("OpenSky error")

    monkeypatch.setattr(api.session, "get", mock_get)

    with pytest.raises(ConnectionError, match="OpenSky API"):
        api.get_aeroplanes("India")

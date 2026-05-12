from unittest.mock import Mock, patch

import pytest
import requests

from src.api import AeroplanesAPI


def test_connect_success() -> None:
    """Проверка успешного подключения к API."""
    api = AeroplanesAPI()

    with patch.object(api.session, "get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        assert api.connect() is True


def test_connect_failure() -> None:
    """Проверка неуспешного подключения к API."""
    api = AeroplanesAPI()

    with patch.object(
        api.session, "get", side_effect=requests.RequestException
    ):
        assert api.connect() is False


def test_get_country_bounding_box_invalid_data() -> None:
    """Проверка ошибки при некорректных данных bounding box."""
    api = AeroplanesAPI()

    with patch.object(api.session, "get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [{"boundingbox": ["1", "2", "3"]}]
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Некорректные данные bounding box"):
            api.get_country_bounding_box("Russia")


def test_get_aeroplanes_empty_states() -> None:
    """Проверка пустого списка самолётов."""
    api = AeroplanesAPI()

    with patch.object(
        api,
        "get_country_bounding_box",
        return_value=(1.0, 2.0, 3.0, 4.0),
    ):
        with patch.object(api.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"states": []}
            mock_get.return_value = mock_response

            result = api.get_aeroplanes("Russia")

            assert result == []


def test_get_aeroplanes_callsign_unknown() -> None:
    """Если callsign отсутствует, должно подставляться Unknown."""
    api = AeroplanesAPI()

    fake_state = [
        "abc123",
        None,
        "Russia",
        111111,
        222222,
        37.6,
        55.7,
        1000.0,
        False,
        250.0,
        180.0,
        0.0,
        None,
        1100.0,
    ]

    with patch.object(
        api,
        "get_country_bounding_box",
        return_value=(1.0, 2.0, 3.0, 4.0),
    ):
        with patch.object(api.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"states": [fake_state]}
            mock_get.return_value = mock_response

            result = api.get_aeroplanes("Russia")

            assert len(result) == 1
            assert result[0]["callsign"] == "Unknown"

from unittest.mock import patch

import pytest

from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver
from src.main import user_interaction
from src.utils import print_aeroplanes


@pytest.fixture
def sample_plane() -> Aeroplane:
    plane_data = [
        {
            "icao24": "abc123",
            "callsign": "SU100",
            "origin_country": "Russia",
            "longitude": 37.6,
            "latitude": 55.7,
            "baro_altitude": 10000.0,
            "on_ground": False,
            "velocity": 250.0,
            "true_track": 180.0,
            "vertical_rate": 0.0,
            "geo_altitude": 10100.0,
        }
    ]
    return Aeroplane.cast_to_object_list(plane_data)[0]


def test_print_aeroplanes_empty(capsys) -> None:
    """Печать пустого списка самолётов."""
    print_aeroplanes([])

    captured = capsys.readouterr()
    assert "Самолеты не найдены." in captured.out


def test_print_aeroplanes_with_limit_message(
    sample_plane: Aeroplane, capsys
) -> None:
    """Печать с ограничением и сообщением о числе показанных записей."""
    planes = [sample_plane, sample_plane, sample_plane]
    print_aeroplanes(planes, limit=2)

    captured = capsys.readouterr()
    assert "1." in captured.out
    assert "2." in captured.out
    assert "Показано 2 из 3 самолетов." in captured.out


def test_json_saver_read_invalid_json(tmp_path) -> None:
    """Если JSON битый, должно возвращаться пустое значение."""
    file_path = tmp_path / "broken.json"
    file_path.write_text("{invalid json}", encoding="utf-8")

    saver = JSONSaver(str(file_path))

    assert saver._read_data() == []


def test_json_saver_get_aeroplanes_with_filter(
    tmp_path, sample_plane: Aeroplane
) -> None:
    """Получение самолётов по фильтру."""
    file_path = tmp_path / "planes.json"
    saver = JSONSaver(str(file_path))
    saver.add_aeroplane(sample_plane)

    result = saver.get_aeroplanes(origin_country="Russia")

    assert len(result) == 1
    assert result[0]["icao24"] == "abc123"


def test_json_saver_delete_aeroplane(tmp_path, sample_plane: Aeroplane) -> None:
    """Удаление самолёта из файла."""
    file_path = tmp_path / "planes.json"
    saver = JSONSaver(str(file_path))
    saver.add_aeroplane(sample_plane)

    saver.delete_aeroplane(sample_plane)
    result = saver.get_aeroplanes()

    assert result == []


def test_user_interaction_empty_country(capsys) -> None:
    """Пустое название страны."""
    with patch("builtins.input", side_effect=["   "]):
        user_interaction()

    captured = capsys.readouterr()
    assert "Название страны не может быть пустым." in captured.out


def test_user_interaction_api_unavailable(capsys) -> None:
    """API недоступно."""
    with patch("builtins.input", side_effect=["Russia"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=False
    ):
        user_interaction()

    captured = capsys.readouterr()
    assert "OpenSky API временно недоступен." in captured.out


def test_user_interaction_no_aeroplanes(capsys) -> None:
    """Самолёты не найдены."""
    with patch("builtins.input", side_effect=["Russia"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=True
    ), patch("src.main.AeroplanesAPI.get_aeroplanes", return_value=[]):
        user_interaction()

    captured = capsys.readouterr()
    assert "Самолеты в указанной зоне не найдены." in captured.out


def test_user_interaction_invalid_menu_choice(sample_plane: Aeroplane, capsys) -> None:
    """Некорректный выбор в меню."""
    plane_dict = [sample_plane.to_dict()]

    with patch("builtins.input", side_effect=["Russia", "9", "0"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=True
    ), patch("src.main.AeroplanesAPI.get_aeroplanes", return_value=plane_dict):
        user_interaction()

    captured = capsys.readouterr()
    assert "Некорректный выбор. Попробуйте снова." in captured.out
    assert "Завершение программы." in captured.out


def test_user_interaction_connection_error(capsys) -> None:
    """Обработка ConnectionError."""
    with patch("builtins.input", side_effect=["Russia"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=True
    ), patch(
        "src.main.AeroplanesAPI.get_aeroplanes",
        side_effect=ConnectionError("network down"),
    ):
        user_interaction()

    captured = capsys.readouterr()
    assert "Ошибка соединения: network down" in captured.out


def test_user_interaction_value_error(capsys) -> None:
    """Обработка ValueError."""
    with patch("builtins.input", side_effect=["Russia"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=True
    ), patch(
        "src.main.AeroplanesAPI.get_aeroplanes",
        side_effect=ValueError("bad input"),
    ):
        user_interaction()

    captured = capsys.readouterr()
    assert "Ошибка ввода: bad input" in captured.out


def test_user_interaction_unexpected_error(capsys) -> None:
    """Обработка непредвиденной ошибки."""
    with patch("builtins.input", side_effect=["Russia"]), patch(
        "src.main.AeroplanesAPI.connect", return_value=True
    ), patch(
        "src.main.AeroplanesAPI.get_aeroplanes",
        side_effect=RuntimeError("boom"),
    ):
        user_interaction()

    captured = capsys.readouterr()
    assert "Непредвиденная ошибка: boom" in captured.out

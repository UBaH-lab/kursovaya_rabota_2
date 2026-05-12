from src.aeroplane import Aeroplane
from src.json_saver import JSONSaver


def test_add_and_get_aeroplane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(str(file_path))

    plane = Aeroplane("abc123", "TEST123", "Germany", 220, 9000, 8800, False)
    saver.add_aeroplane(plane)

    data = saver.get_aeroplanes()
    assert len(data) == 1
    assert data[0]["callsign"] == "TEST123"


def test_delete_aeroplane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(str(file_path))

    plane = Aeroplane("abc123", "TEST123", "Germany", 220, 9000, 8800, False)
    saver.add_aeroplane(plane)
    saver.delete_aeroplane(plane)

    data = saver.get_aeroplanes()
    assert data == []


def test_no_duplicates(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(str(file_path))

    plane = Aeroplane("abc123", "TEST123", "Germany", 220, 9000, 8800, False)
    saver.add_aeroplane(plane)
    saver.add_aeroplane(plane)

    data = saver.get_aeroplanes()
    assert len(data) == 1

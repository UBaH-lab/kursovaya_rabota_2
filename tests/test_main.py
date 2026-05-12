from src.main import user_interaction


def test_main_empty_country(monkeypatch, capsys):
    inputs = iter([""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    user_interaction()
    captured = capsys.readouterr()
    assert "не может быть пустым" in captured.out


def test_main_api_unavailable(monkeypatch, capsys):
    inputs = iter(["India"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    class MockAPI:
        def connect(self):
            return False

    monkeypatch.setattr("src.main.AeroplanesAPI", lambda: MockAPI())

    user_interaction()
    captured = capsys.readouterr()
    assert "временно недоступен" in captured.out


def test_main_no_aeroplanes(monkeypatch, capsys):
    inputs = iter(["India"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    class MockAPI:
        def connect(self):
            return True

        def get_aeroplanes(self, country):
            return []

    class MockSaver:
        def add_aeroplane(self, plane):
            pass

    monkeypatch.setattr("src.main.AeroplanesAPI", lambda: MockAPI())
    monkeypatch.setattr("src.main.JSONSaver", lambda: MockSaver())

    user_interaction()
    captured = capsys.readouterr()
    assert "не найдены" in captured.out


def test_main_exit_immediately(monkeypatch, capsys):
    inputs = iter(["India", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    class MockAPI:
        def connect(self):
            return True

        def get_aeroplanes(self, country):
            return [
                {
                    "icao24": "abc123",
                    "callsign": "TEST123",
                    "origin_country": "India",
                    "velocity": 250,
                    "geo_altitude": 10000,
                    "baro_altitude": 9800,
                    "on_ground": False,
                }
            ]

    class MockSaver:
        def add_aeroplane(self, plane):
            pass

    monkeypatch.setattr("src.main.AeroplanesAPI", lambda: MockAPI())
    monkeypatch.setattr("src.main.JSONSaver", lambda: MockSaver())

    user_interaction()
    captured = capsys.readouterr()
    assert "Найдено самолетов: 1" in captured.out
    assert "Завершение программы." in captured.out


def test_main_invalid_menu_choice(monkeypatch, capsys):
    inputs = iter(["India", "99", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    class MockAPI:
        def connect(self):
            return True

        def get_aeroplanes(self, country):
            return [
                {
                    "icao24": "abc123",
                    "callsign": "TEST123",
                    "origin_country": "India",
                    "velocity": 250,
                    "geo_altitude": 10000,
                    "baro_altitude": 9800,
                    "on_ground": False,
                }
            ]

    class MockSaver:
        def add_aeroplane(self, plane):
            pass

    monkeypatch.setattr("src.main.AeroplanesAPI", lambda: MockAPI())
    monkeypatch.setattr("src.main.JSONSaver", lambda: MockSaver())

    user_interaction()
    captured = capsys.readouterr()
    assert "Некорректный выбор" in captured.out


def test_main_connection_error(monkeypatch, capsys):
    inputs = iter(["India"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    class MockAPI:
        def connect(self):
            return True

        def get_aeroplanes(self, country):
            raise ConnectionError("API error")

    class MockSaver:
        def add_aeroplane(self, plane):
            pass

    monkeypatch.setattr("src.main.AeroplanesAPI", lambda: MockAPI())
    monkeypatch.setattr("src.main.JSONSaver", lambda: MockSaver())

    user_interaction()
    captured = capsys.readouterr()
    assert "Ошибка соединения" in captured.out

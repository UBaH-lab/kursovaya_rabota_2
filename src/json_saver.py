import json
import os

from src.aeroplane import Aeroplane
from src.file_base import BaseSaver


class JSONSaver(BaseSaver):
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        directory = os.path.dirname(self.filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def _read_data(self) -> list[dict]:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: list[dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_data()

        if not any(item.get("icao24") == aeroplane.icao24 for item in data):
            data.append(aeroplane.to_dict())
            self._write_data(data)

    def get_aeroplanes(self, **kwargs) -> list[dict]:
        data = self._read_data()

        if not kwargs:
            return data

        result = []
        for item in data:
            if all(item.get(key) == value for key, value in kwargs.items()):
                result.append(item)
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_data()
        filtered_data = [
            item for item in data if item.get("icao24") != aeroplane.icao24
        ]
        self._write_data(filtered_data)

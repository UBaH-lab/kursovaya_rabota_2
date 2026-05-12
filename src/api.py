from typing import Any

import requests

from src.api_base import BaseAPI


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API Nominatim и OpenSky."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "coursework-airplanes-app/1.0"})

    def connect(self) -> bool:
        """Проверяет доступность OpenSky API."""
        try:
            response = self.session.get(self.OPENSKY_URL, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_country_bounding_box(
            self, country: str
    ) -> tuple[float, float, float, float]:
        """Получает координаты страны через Nominatim API."""
        params: dict[str, str | int] = {}
        params["q"] = country
        params["format"] = "json"
        params["limit"] = 1

        try:
            response = self.session.get(self.NOMINATIM_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise ValueError(f"Страна '{country}' не найдена")

            bounding_box = data[0].get("boundingbox")
            if not bounding_box or len(bounding_box) != 4:
                raise ValueError("Некорректные данные bounding box")

            south, north, west, east = map(float, bounding_box)
            return south, north, west, east

        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к Nominatim API: {e}") from e

    def get_aeroplanes(self, country: str) -> list[dict[str, Any]]:
        """Получает данные о самолетах в воздушном пространстве страны."""
        south, north, west, east = self.get_country_bounding_box(country)

        params = {"lamin": south, "lamax": north, "lomin": west, "lomax": east}

        try:
            response = self.session.get(self.OPENSKY_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            states = data.get("states", [])
            aeroplanes = []

            for state in states:
                aeroplane_data = {
                    "icao24": state[0],
                    "callsign": state[1].strip() if state[1] else "Unknown",
                    "origin_country": state[2],
                    "time_position": state[3],
                    "last_contact": state[4],
                    "longitude": state[5],
                    "latitude": state[6],
                    "baro_altitude": state[7],
                    "on_ground": state[8],
                    "velocity": state[9],
                    "true_track": state[10],
                    "vertical_rate": state[11],
                    "geo_altitude": state[13],
                }
                aeroplanes.append(aeroplane_data)

            return aeroplanes

        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к OpenSky API: {e}") from e

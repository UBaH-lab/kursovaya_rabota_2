from __future__ import annotations


class Aeroplane:
    """Класс для работы с информацией о самолете."""

    __slots__ = (
        "_icao24",
        "_callsign",
        "_origin_country",
        "_velocity",
        "_geo_altitude",
        "_baro_altitude",
        "_on_ground",
    )

    def __init__(
        self,
        icao24: str,
        callsign: str,
        origin_country: str,
        velocity: float | None,
        geo_altitude: float | None,
        baro_altitude: float | None,
        on_ground: bool,
    ) -> None:
        self.icao24 = icao24
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = velocity
        self.geo_altitude = geo_altitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground

    @property
    def icao24(self) -> str:
        return self._icao24

    @icao24.setter
    def icao24(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("icao24 должен быть непустой строкой")
        self._icao24 = value.strip()

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        if value is None:
            value = "Unknown"
        if not isinstance(value, str):
            raise ValueError("callsign должен быть строкой")
        self._callsign = value.strip() or "Unknown"

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("origin_country должен быть непустой строкой")
        self._origin_country = value.strip()

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float | None) -> None:
        if value is None:
            value = 0.0
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("velocity должна быть числом >= 0")
        self._velocity = float(value)

    @property
    def geo_altitude(self) -> float:
        return self._geo_altitude

    @geo_altitude.setter
    def geo_altitude(self, value: float | None) -> None:
        if value is None:
            value = 0.0
        if not isinstance(value, (int, float)):
            raise ValueError("geo_altitude должна быть числом")
        self._geo_altitude = float(value)

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude

    @baro_altitude.setter
    def baro_altitude(self, value: float | None) -> None:
        if value is None:
            value = 0.0
        if not isinstance(value, (int, float)):
            raise ValueError("baro_altitude должна быть числом")
        self._baro_altitude = float(value)

    @property
    def on_ground(self) -> bool:
        return self._on_ground

    @on_ground.setter
    def on_ground(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("on_ground должен быть bool")
        self._on_ground = value

    def to_dict(self) -> dict:
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude,
            "baro_altitude": self.baro_altitude,
            "on_ground": self.on_ground,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aeroplane":
        return cls(
            icao24=data["icao24"],
            callsign=data.get("callsign", "Unknown"),
            origin_country=data["origin_country"],
            velocity=data.get("velocity"),
            geo_altitude=data.get("geo_altitude"),
            baro_altitude=data.get("baro_altitude"),
            on_ground=data.get("on_ground", False),
        )

    @classmethod
    def cast_to_object_list(cls, aeroplanes_data: list[dict]) -> list["Aeroplane"]:
        result = []
        for item in aeroplanes_data:
            try:
                result.append(cls.from_dict(item))
            except (ValueError, KeyError):
                continue
        return result

    def is_faster_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с Aeroplane")
        return self.velocity > other.velocity

    def is_higher_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с Aeroplane")
        return self.geo_altitude > other.geo_altitude

    def __lt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.geo_altitude) < (other.velocity, other.geo_altitude)

    def __le__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.geo_altitude) <= (
            other.velocity,
            other.geo_altitude,
        )

    def __gt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.geo_altitude) > (other.velocity, other.geo_altitude)

    def __ge__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity, self.geo_altitude) >= (
            other.velocity,
            other.geo_altitude,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return False
        return (
            self.icao24 == other.icao24
            and self.callsign == other.callsign
            and self.origin_country == other.origin_country
            and self.velocity == other.velocity
            and self.geo_altitude == other.geo_altitude
        )

    def __str__(self) -> str:
        return (
            f"Позывной: {self.callsign}, "
            f"Страна регистрации: {self.origin_country}, "
            f"Скорость: {self.velocity} м/с, "
            f"Высота: {self.geo_altitude} м, "
            f"На земле: {'Да' if self.on_ground else 'Нет'}"
        )

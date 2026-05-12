from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def connect(self) -> bool:
        """Проверяет доступность API."""
        pass

    @abstractmethod
    def get_country_bounding_box(
        self, country: str
    ) -> tuple[float, float, float, float]:
        """
        Получает bounding box страны в формате:
        (south, north, west, east)
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[dict]:
        """Получает список самолетов для заданной страны."""
        pass

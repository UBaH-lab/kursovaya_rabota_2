from abc import ABC, abstractmethod

from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для работы с хранилищем самолетов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(self, **kwargs) -> list[dict]:
        """Получает самолеты по критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолет из хранилища."""
        pass

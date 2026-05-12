from src.aeroplane import Aeroplane


def filter_aeroplanes_by_country(
    aeroplanes: list[Aeroplane], countries: list[str]
) -> list[Aeroplane]:
    """Фильтрация самолетов по стране регистрации."""
    countries_lower = {
        country.strip().lower() for country in countries if country.strip()
    }
    return [
        plane for plane in aeroplanes if plane.origin_country.lower() in countries_lower
    ]


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane], min_altitude: float, max_altitude: float
) -> list[Aeroplane]:
    """Фильтрация самолетов по диапазону высот."""
    if min_altitude > max_altitude:
        raise ValueError("Минимальная высота не может быть больше максимальной")

    return [
        plane
        for plane in aeroplanes
        if min_altitude <= plane.geo_altitude <= max_altitude
    ]


def get_airborne_aeroplanes(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Возвращает только самолеты, находящиеся в воздухе."""
    return [plane for plane in aeroplanes if not plane.on_ground]


def get_airborne_with_positive_altitude(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Возвращает только самолеты в воздухе с высотой больше 0."""
    return [
        plane for plane in aeroplanes if not plane.on_ground and plane.geo_altitude > 0
    ]


def sort_aeroplanes_by_altitude_desc(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортировка самолетов по высоте по убыванию."""
    return sorted(aeroplanes, key=lambda plane: plane.geo_altitude, reverse=True)


def sort_aeroplanes_by_velocity_desc(aeroplanes: list[Aeroplane]) -> list[Aeroplane]:
    """Сортировка самолетов по скорости по убыванию."""
    return sorted(aeroplanes, key=lambda plane: plane.velocity, reverse=True)


def get_top_aeroplanes(aeroplanes: list[Aeroplane], top_n: int) -> list[Aeroplane]:
    """Получение топ N самолетов."""
    if top_n <= 0:
        raise ValueError("top_n должен быть больше 0")
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: list[Aeroplane], limit: int | None = None) -> None:
    """Печать списка самолетов."""
    if not aeroplanes:
        print("Самолеты не найдены.")
        return

    planes_to_print = aeroplanes if limit is None else aeroplanes[:limit]

    for i, plane in enumerate(planes_to_print, start=1):
        print(f"{i}. {plane}")

    if limit is not None and len(aeroplanes) > limit:
        print(f"\nПоказано {limit} из {len(aeroplanes)} самолетов.")

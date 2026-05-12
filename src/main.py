from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.json_saver import JSONSaver
from src.utils import (
    filter_aeroplanes_by_country,
    get_aeroplanes_by_altitude,
    get_airborne_aeroplanes,
    get_airborne_with_positive_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes_by_altitude_desc,
    sort_aeroplanes_by_velocity_desc,
)


def user_interaction() -> None:
    """Функция взаимодействия с пользователем через консоль."""
    api = AeroplanesAPI()
    saver = JSONSaver()

    try:
        country = input("Введите название страны: ").strip()
        if not country:
            print("Название страны не может быть пустым.")
            return

        print("Проверяем доступность API...")
        if not api.connect():
            print("OpenSky API временно недоступен.")
            return

        print("Получаем данные о самолетах...")
        aeroplanes_data = api.get_aeroplanes(country)
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

        if not aeroplanes:
            print("Самолеты в указанной зоне не найдены.")
            return

        for plane in aeroplanes:
            saver.add_aeroplane(plane)

        print(f"Найдено самолетов: {len(aeroplanes)}")

        while True:
            print("\nВыберите действие:")
            print("1. Показать топ N самолетов по высоте")
            print("2. Отфильтровать самолеты по стране регистрации")
            print("3. Отфильтровать самолеты по диапазону высот")
            print("4. Показать все самолеты (первые 20)")
            print("5. Показать только самолеты в воздухе (первые 20)")
            print("6. Показать топ N самолетов по скорости")
            print("7. Показать только самолеты в воздухе с высотой > 0")
            print("0. Выход")

            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                try:
                    top_n = int(input("Введите количество самолетов: "))
                    sorted_planes = sort_aeroplanes_by_altitude_desc(aeroplanes)
                    top_planes = get_top_aeroplanes(sorted_planes, top_n)
                    print_aeroplanes(top_planes)
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "2":
                countries = input("Введите страны регистрации через запятую: ").split(
                    ","
                )
                filtered = filter_aeroplanes_by_country(aeroplanes, countries)
                print_aeroplanes(filtered, limit=20)

            elif choice == "3":
                try:
                    min_altitude = float(input("Введите минимальную высоту: "))
                    max_altitude = float(input("Введите максимальную высоту: "))
                    filtered = get_aeroplanes_by_altitude(
                        aeroplanes, min_altitude, max_altitude
                    )
                    print_aeroplanes(filtered, limit=20)
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "4":
                print_aeroplanes(aeroplanes, limit=20)

            elif choice == "5":
                airborne = get_airborne_aeroplanes(aeroplanes)
                print_aeroplanes(airborne, limit=20)

            elif choice == "6":
                try:
                    top_n = int(input("Введите количество самолетов: "))
                    sorted_planes = sort_aeroplanes_by_velocity_desc(aeroplanes)
                    top_planes = get_top_aeroplanes(sorted_planes, top_n)
                    print_aeroplanes(top_planes)
                except ValueError as e:
                    print(f"Ошибка: {e}")

            elif choice == "7":
                airborne_positive = get_airborne_with_positive_altitude(aeroplanes)
                print_aeroplanes(airborne_positive, limit=20)

            elif choice == "0":
                print("Завершение программы.")
                break

            else:
                print("Некорректный выбор. Попробуйте снова.")

    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    user_interaction()

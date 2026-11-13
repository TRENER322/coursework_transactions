import json
import os
from typing import Optional

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import simple_search
from src.utils import read_transactions_excel
from src.views import main_page


def load_settings() -> dict:
    """Загружает настройки пользователя из JSON-файла."""
    settings_file = "user_settings.json"
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"],
    }


def get_date_input(prompt: str, default_date: Optional[str] = None) -> Optional[str]:
    """Безопасно запрашивает дату у пользователя."""
    date_str = input(prompt).strip()
    if not date_str:
        return default_date
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print("Ошибка: неверный формат даты. Используйте ГГГГ-ММ-ДД.")
        return None


def main() -> None:
    """Главная функция, управляющая программой."""
    print("Загрузка данных из Excel...")
    df = read_transactions_excel("data/operations.xls")

    if df.empty:
        print("Не удалось загрузить данные. Проверьте файл data/operations.xls")
        return

    settings = load_settings()

    while True:
        print("\n" + "=" * 40)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. Главная страница (JSON)")
        print("2. Простой поиск")
        print("3. Траты по категории")
        print("4. Средние траты по дням недели")
        print("5. Средние траты в рабочий/выходной день")
        print("0. Выход")
        print("=" * 40)

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            print("\n--- ГЛАВНАЯ СТРАНИЦА ---")
            date_input = input(
                "Введите дату и время (ГГГГ-ММ-ДД ЧЧ:ММ:СС) или Enter для примера из 2021 года: "
            ).strip()

            # Используем отдельное имя переменной, чтобы не конфликтовать с date_str ниже
            if not date_input:
                date_main = "2021-12-31 23:59:59"
            else:
                if len(date_input) == 10:
                    date_main = date_input + " 00:00:00"
                else:
                    date_main = date_input

            try:
                result_json = main_page(df, settings, date_main)
                print(result_json)
            except Exception as e:
                print(f"Ошибка при генерации страницы: {e}")

        elif choice == "2":
            print("\n--- ПРОСТОЙ ПОИСК ---")
            search_term = input("Введите строку для поиска (например, 'Магнит'): ").strip()
            result_json = simple_search(df, search_term)
            result = json.loads(result_json)
            if not result:
                print("Ничего не найдено.")
            else:
                print(f"Найдено {len(result)} транзакций:")
                for item in result[:10]:
                    print(
                        f"  {item.get('Дата операции')} | {item.get('Категория')} | "
                        f"{item.get('Описание')} | {item.get('Сумма операции')} руб."
                    )

        elif choice == "3":
            print("\n--- ТРАТЫ ПО КАТЕГОРИИ ---")
            category = input("Введите название категории (например, 'Супермаркеты'): ").strip()
            date_cat = get_date_input(
                "Введите дату (ГГГГ-ММ-ДД) или оставьте пустым для текущей: ",
                default_date="2021-12-31",
            )
            if date_cat is None:
                continue

            result = spending_by_category(df, category, date_cat)
            if result.empty:
                print("Траты по этой категории не найдены.")
            else:
                total = result["Сумма операции"].sum()
                print(f"Найдено {len(result)} операций. Общая сумма: {total:.2f} руб.")

        elif choice == "4":
            print("\n--- СРЕДНИЕ ТРАТЫ ПО ДНЯМ НЕДЕЛИ ---")
            date_weekday = get_date_input(
                "Введите дату (ГГГГ-ММ-ДД) или оставьте пустым для текущей: ",
                default_date="2021-12-31",
            )
            if date_weekday is None:
                continue
            result = spending_by_weekday(df, date_weekday)
            print(result)

        elif choice == "5":
            print("\n--- СРЕДНИЕ ТРАТЫ В РАБОЧИЙ/ВЫХОДНОЙ ДЕНЬ ---")
            date_workday = get_date_input(
                "Введите дату (ГГГГ-ММ-ДД) или оставьте пустым для текущей: ",
                default_date="2021-12-31",
            )
            if date_workday is None:
                continue
            result = spending_by_workday(df, date_workday)
            print(result)

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()

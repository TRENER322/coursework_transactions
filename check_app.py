import json

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import simple_search
from src.utils import read_transactions_excel
from src.views import main_page


def run_checks():
    print("=" * 60)
    print("1. ПРОВЕРКА ЧТЕНИЯ ФАЙЛА")
    print("=" * 60)
    df = read_transactions_excel("data/operations.xls")
    if df.empty:
        print("❌ Ошибка: файл пуст или не найден.")
        return
    print(f"✅ Данные загружены. Строк: {len(df)}\n")

    print("=" * 60)
    print("2. ПРОВЕРКА ГЛАВНОЙ СТРАНИЦЫ (views.py)")
    print("=" * 60)
    settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"]
    }

    # Вызываем главную страницу на дату из файла
    result_json = main_page(df, settings, "2021-12-31 23:59:59")
    data = json.loads(result_json)

    print(f"Приветствие: {data['greeting']}")
    print(f"Карты: {data['cards']}")
    print(f"Топ-5 транзакций: {len(data['top_transactions'])} шт.")
    print(f"Курсы валют: {data['currency_rates']}")
    print(f"Акции: {data['stock_prices']}")
    print(f"Расходы/Доходы: {data['expenses']}\n")

    print("=" * 60)
    print("3. ПРОВЕРКА СЕРВИСА ПОИСКА (services.py)")
    print("=" * 60)
    search_term = "Магнит"
    search_result_json = simple_search(df, search_term)
    search_result = json.loads(search_result_json)

    print(f"Поиск по слову '{search_term}': найдено {len(search_result)} записей.")
    if search_result:
        print(f"Пример: {search_result[0].get('Описание')} | {search_result[0].get('Сумма операции')} руб.\n")

    print("=" * 60)
    print("4. ПРОВЕРКА ОТЧЕТОВ (reports.py)")
    print("=" * 60)

    cat_report = spending_by_category(df, "Супермаркеты", "2021-12-31")
    print(f"Траты по категории 'Супермаркеты': найдено {len(cat_report)} операций.")

    weekday_report = spending_by_weekday(df, "2021-12-31")
    print(f"Средние траты по дням недели:\n{weekday_report}\n")

    workday_report = spending_by_workday(df, "2021-12-31")
    print(f"Средние траты в рабочие/выходные:\n{workday_report}\n")


if __name__ == "__main__":
    run_checks()

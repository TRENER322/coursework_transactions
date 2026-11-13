import json

import pandas as pd


def simple_search(transactions: pd.DataFrame, search_string: str) -> str:
    """
    Ищет транзакции по подстроке в описании или категории (без учета регистра).
    Возвращает JSON-строку.
    """
    if transactions.empty or not search_string:
        return "[]"

    search_lower = search_string.lower()
    records = transactions.to_dict(orient="records")

    # Используем функциональное программирование (filter + lambda)
    filtered_data = list(
        filter(
            lambda x: search_lower in str(x.get("Описание", "")).lower()
            or search_lower in str(x.get("Категория", "")).lower(),
            records,
        )
    )

    return json.dumps(filtered_data, ensure_ascii=False, default=str)

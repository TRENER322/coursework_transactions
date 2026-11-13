import json

import pandas as pd

from src.services import simple_search


def test_simple_search():
    df = pd.DataFrame({
        "Описание": ["Магнит", "Пятерочка", "Такси"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"]
    })

    # 1. Ищем "маг" (должно найти 1 шт без учета регистра)
    result_json = simple_search(df, "маг")
    result = json.loads(result_json)  # Превращаем JSON-строку обратно в список

    assert len(result) == 1
    assert result[0]["Описание"] == "Магнит"

    # 2. Ищем "супер" (должно найти 2 шт по категории)
    result_cat_json = simple_search(df, "супер")
    result_cat = json.loads(result_cat_json)

    assert len(result_cat) == 2
    assert result_cat[0]["Категория"] == "Супермаркеты"
    assert result_cat[1]["Категория"] == "Супермаркеты"

    # 3. Пустой результат (должен вернуть пустой JSON-массив [])
    empty_result_json = simple_search(df, "Кино")
    empty_result = json.loads(empty_result_json)

    assert empty_result == []

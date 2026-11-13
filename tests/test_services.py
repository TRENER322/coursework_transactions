import pandas as pd

from src.services import simple_search


def test_simple_search():
    df = pd.DataFrame({
        "Описание": ["Магнит", "Пятерочка", "Такси"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"]
    })

    # Ищем "маг" (должно найти Магнит без учета регистра)
    result = simple_search(df, "маг")
    assert len(result) == 1
    assert result.iloc[0]["Описание"] == "Магнит"

    # Ищем "супер" (должно найти 2 шт по категории)
    result_cat = simple_search(df, "супер")
    assert len(result_cat) == 2

    # Пустой результат
    empty_result = simple_search(df, "Кино")
    assert empty_result.empty

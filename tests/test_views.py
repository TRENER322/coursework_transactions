import json

import pandas as pd
import pytest

from src.views import main_page


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Дата операции": ["01.12.2023 12:00:00", "02.12.2023 14:00:00"],
        "Номер карты": ["*1234", "*1234"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-1000.0, 2000.0],
        "Кэшбэк": [10.0, 0.0],
        "Категория": ["Супермаркеты", "Пополнение"],
        "Описание": ["Магнит", "Перевод"]
    })


def test_main_page(sample_df):
    settings = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    result_json = main_page(sample_df, settings, "2023-12-15 12:00:00")
    result = json.loads(result_json)

    assert "greeting" in result
    assert len(result["cards"]) > 0
    assert len(result["top_transactions"]) <= 5
    assert "currency_rates" in result
    assert "stock_prices" in result
    assert "expenses" in result

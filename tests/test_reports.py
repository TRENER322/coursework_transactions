import os
from datetime import datetime

import pandas as pd
import pytest

from src.reports import (save_report, spending_by_category,
                         spending_by_weekday, spending_by_workday)


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    data = {
        "Дата операции": [
            "01.12.2021 10:00:00",
            "02.12.2021 11:00:00",
            "03.12.2021 12:00:00",  # Пятница
            "04.12.2021 13:00:00",  # Суббота
            "05.12.2021 14:00:00",  # Воскресенье
            "06.12.2021 15:00:00",
            "07.12.2021 16:00:00",
            "08.12.2021 17:00:00",
        ],
        "Сумма операции": [-100, -200, -300, -400, -500, -600, -700, -800],
        "Категория": [
            "Супермаркеты",
            "Супермаркеты",
            "Кафе",
            "Кафе",
            "Супермаркеты",
            "Транспорт",
            "Супермаркеты",
            "Развлечения",
        ],
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_transactions):
    """Тест трат по категории."""
    result = spending_by_category(sample_transactions, "Супермаркеты", "2021-12-31")
    assert len(result) == 4
    assert all(result["Категория"] == "Супермаркеты")
    # Проверяем, что даты входят в диапазон (с 31.09.2021 по 31.12.2021)
    assert (result["Дата операции"] >= datetime(2021, 9, 30)).all()


def test_spending_by_category_empty(sample_transactions):
    """Тест: категория не найдена."""
    result = spending_by_category(sample_transactions, "Несуществующая", "2021-12-31")
    assert result.empty


def test_spending_by_weekday(sample_transactions):
    """Тест средних трат по дням недели."""
    result = spending_by_weekday(sample_transactions, "2021-12-31")
    assert not result.empty
    assert "День недели" in result.columns
    assert "Средняя сумма" in result.columns
    # Проверяем, что есть хотя бы один день недели
    assert len(result) > 0


def test_spending_by_workday(sample_transactions):
    """Тест средних трат в рабочие/выходные дни."""
    result = spending_by_workday(sample_transactions, "2021-12-31")
    assert not result.empty
    assert "Тип дня" in result.columns
    assert "Средняя сумма" in result.columns
    # В наших данных есть и рабочие, и выходные дни
    assert len(result) == 2


def test_save_report_decorator(sample_transactions):
    """Тест декоратора сохранения отчета."""
    # Удаляем файл, если он существует
    test_file = "test_report.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    @save_report(filename=test_file)
    def dummy_report(df, category, date):
        return spending_by_category(df, category, date)

    dummy_report(sample_transactions, "Супермаркеты", "2021-12-31")

    # Проверяем, что файл создан и в нем есть данные
    assert os.path.exists(test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Дата операции" in content
        assert "Сумма операции" in content

    os.remove(test_file)


def test_save_report_decorator_without_params(sample_transactions):
    """Тест декоратора без параметров (имя файла по умолчанию)."""
    default_file = "dummy_report_report.txt"
    if os.path.exists(default_file):
        os.remove(default_file)

    @save_report
    def dummy_report(df, category, date):
        return spending_by_category(df, category, date)

    dummy_report(sample_transactions, "Супермаркеты", "2021-12-31")

    assert os.path.exists(default_file)

    os.remove(default_file)

import functools
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_DIR / "reports.log", mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def save_report(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения результата отчета в файл.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            file_to_write = filename if filename else f"{func.__name__}_report.txt"

            try:
                with open(file_to_write, "w", encoding="utf-8") as f:
                    f.write(str(result))
                logger.info("Отчет успешно сохранен в %s", file_to_write)
            except Exception as e:
                logger.error("Ошибка сохранения отчета: %s", e)

            return result

        return wrapper

    if callable(filename):
        func = filename
        filename = None
        return decorator(func)

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.
    """
    logger.debug("Расчет трат по категории: %s", category)
    end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    start_date = end_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Категория"] == category) &
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]
    return filtered_df


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца.
    """
    logger.debug("Расчет средних трат по дням недели")
    end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    start_date = end_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ].copy()

    filtered_df["День недели"] = filtered_df["Дата операции"].dt.day_name()
    result = filtered_df.groupby("День недели")["Сумма операции"].mean().reset_index()
    result.columns = ["День недели", "Средняя сумма"]

    return result


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и в выходной день за последние три месяца.
    """
    logger.debug("Расчет средних трат в рабочие/выходные дни")
    end_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    start_date = end_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ].copy()

    filtered_df["Тип дня"] = filtered_df["Дата операции"].dt.day_of_week.apply(
        lambda x: "Выходной" if x >= 5 else "Рабочий"
    )

    result = filtered_df.groupby("Тип дня")["Сумма операции"].mean().reset_index()
    result.columns = ["Тип дня", "Средняя сумма"]

    return result

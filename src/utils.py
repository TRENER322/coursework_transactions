import logging
from pathlib import Path

import pandas as pd

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def read_transactions_excel(file_path: str) -> pd.DataFrame:
    """
    Читает транзакции из Excel-файла и возвращает DataFrame.
    """
    logger.debug("Чтение Excel-файла: %s", file_path)
    try:
        df = pd.read_excel(file_path)
        logger.info("Excel-файл успешно прочитан. Записей: %d", len(df))
        return df
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return pd.DataFrame()
    except Exception as e:
        logger.error("Ошибка чтения Excel: %s", e)
        return pd.DataFrame()

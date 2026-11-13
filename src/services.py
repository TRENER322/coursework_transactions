import pandas as pd


def simple_search(transactions: pd.DataFrame, search_string: str) -> pd.DataFrame:
    """
    Ищет транзакции по подстроке в описании или категории (без учета регистра).
    """
    if transactions.empty or not search_string:
        return pd.DataFrame()

    # Ищем в колонках Описание и Категория
    mask = (
            transactions["Описание"].str.contains(search_string, case=False, na=False) |
            transactions["Категория"].str.contains(search_string, case=False, na=False)
    )

    return transactions[mask]

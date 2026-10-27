import pandas as pd
from src.reports import spending_by_category, spending_by_weekday

def test_spending_by_category() -> None:
    df = pd.DataFrame({
        "Дата операции": ["01.05.2023 12:00:00", "01.05.2023 13:00:00"],
        "Категория": ["Кафе", "Кафе"],
        "Сумма операции": [-1000.0, -500.0],
    })
    res = spending_by_category(df, "Кафе", "2023-05-20")
    assert "1500" in res

def test_spending_by_weekday() -> None:
    df = pd.DataFrame({
        "Дата операции": ["01.05.2023 12:00:00"],
        "Категория": ["Кафе"],
        "Сумма операции": [-1000.0],
    })
    res = spending_by_weekday(df, "2023-05-20")
    assert "Понедельник" in res
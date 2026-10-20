import json
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable

import pandas as pd
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


def save_report(filename: str) -> Callable:
    """Декоратор для сохранения результата в файл."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(result)
            except Exception as e:
                logger.error(f"Ошибка записи отчета: {e}")
            return result

        return wrapper

    return decorator


def _get_prepared_df(df: pd.DataFrame, date_str: str | None) -> pd.DataFrame:
    """Вспомогательная функция для фильтрации трат за 3 месяца."""
    end_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
    start_date = end_date - relativedelta(months=3)

    df = df.copy()
    df["Дата операции"] = pd.to_datetime(
        df["Дата операции"], dayfirst=True, errors="coerce"
    )

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    filtered = df.loc[mask]

    # Только траты
    filtered = filtered[filtered["Сумма операции"] < 0]
    filtered["Сумма операции"] = filtered["Сумма операции"].abs()
    return filtered


@save_report("report_category.json")
def spending_by_category(
    transactions: pd.DataFrame, category: str, date_str: str | None = None
) -> str:
    """Траты по категории за 3 месяца."""
    df = _get_prepared_df(transactions, date_str)
    filtered = df[df["Категория"] == category]
    total = float(filtered["Сумма операции"].sum())
    return json.dumps(
        {"category": category, "total": round(total, 2)}, ensure_ascii=False
    )


@save_report("report_weekday.json")
def spending_by_weekday(transactions: pd.DataFrame, date_str: str | None = None) -> str:
    """Средние траты по дням недели."""
    df = _get_prepared_df(transactions, date_str)
    df["weekday"] = df["Дата операции"].dt.dayofweek
    grouped = df.groupby("weekday")["Сумма операции"].mean().round(2)

    days = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }
    res = {days[k]: float(v) for k, v in grouped.items()}
    return json.dumps(res, ensure_ascii=False)


@save_report("report_weekend.json")
def spending_weekday_vs_weekend(
    transactions: pd.DataFrame, date_str: str | None = None
) -> str:
    """Средние траты в рабочий и выходной день."""
    df = _get_prepared_df(transactions, date_str)
    df["weekday"] = df["Дата операции"].dt.dayofweek
    df["day_type"] = df["weekday"].apply(lambda x: "Выходной" if x >= 5 else "Рабочий")

    grouped = df.groupby("day_type")["Сумма операции"].mean().round(2)
    return json.dumps({k: float(v) for k, v in grouped.items()}, ensure_ascii=False)

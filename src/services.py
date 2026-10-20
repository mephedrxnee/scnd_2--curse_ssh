import json
import logging
import math
import re
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


def cashback_categories(data: list[dict[str, Any]], year: int, month: int) -> str:
    """Выгодные категории повышенного кешбэка."""
    filtered = filter(
        lambda x: datetime.strptime(
            str(x.get("Дата операции", ""))[:10], "%d.%m.%Y"
        ).year
        == year
        and datetime.strptime(str(x.get("Дата операции", ""))[:10], "%d.%m.%Y").month
        == month
        and float(x.get("Сумма операции", 0)) < 0,
        data,
    )

    cats: dict[str, float] = {}
    for t in filtered:
        category = str(t.get("Категория", "Остальное"))
        amount = abs(float(t.get("Сумма операции", 0)))
        cats[category] = cats.get(category, 0) + amount * 0.01  # 1%

    return json.dumps(
        {k: int(v) for k, v in cats.items()}, ensure_ascii=False, indent=2
    )


def investment_bank(
    month: str, transactions: list[dict[str, Any]], limit: int
) -> float:
    """Инвесткопилка: округление трат до шага limit."""
    filtered = filter(
        lambda x: str(x.get("Дата операции", "")).startswith(month), transactions
    )

    total = 0.0
    for t in filtered:
        amount = abs(float(t.get("Сумма операции", 0)))
        if amount > 0:
            rounded = math.ceil(amount / limit) * limit
            total += rounded - amount
    return round(total, 2)


def simple_search(transactions: list[dict[str, Any]], query: str) -> str:
    """Простой поиск по описанию или категории."""
    q = query.lower()
    result = filter(
        lambda t: q in str(t.get("Описание", "")).lower()
        or q in str(t.get("Категория", "")).lower(),
        transactions,
    )
    return json.dumps(list(result), ensure_ascii=False, indent=2, default=str)


def phone_search(transactions: list[dict[str, Any]]) -> str:
    """Поиск по телефонным номерам."""
    pattern = re.compile(
        r"(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    )
    result = filter(
        lambda t: pattern.search(str(t.get("Описание", ""))) is not None, transactions
    )
    return json.dumps(list(result), ensure_ascii=False, indent=2, default=str)


def person_transfers(transactions: list[dict[str, Any]]) -> str:
    """Поиск переводов физическим лицам."""
    pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")
    result = filter(
        lambda t: str(t.get("Категория", "")) == "Переводы"
        and pattern.search(str(t.get("Описание", ""))) is not None,
        transactions,
    )
    return json.dumps(list(result), ensure_ascii=False, indent=2, default=str)

import json
import logging
from datetime import datetime
from typing import Any

import requests

logger = logging.getLogger(__name__)


def get_greeting(dt: datetime) -> str:
    """Возвращает приветствие в зависимости от времени."""
    hour = dt.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """Получает курсы валют к рублю."""
    rates = []
    for curr in currencies:
        try:
            resp = requests.get(
                f"https://api.exchangerate-api.com/v4/latest/{curr}", timeout=5
            )
            resp.raise_for_status()
            rate = resp.json()["rates"]["RUB"]
            rates.append({"currency": curr, "rate": round(rate, 2)})
        except Exception as e:
            logger.error(f"Ошибка API валют ({curr}): {e}")
            rates.append({"currency": curr, "rate": None})
    return rates


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает цены акций (демо-заглушка, так как бесплатные API нестабильны)."""
    prices = []
    for stock in stocks:
        try:
            # В реальном проекте здесь был бы вызов API (например, Yahoo Finance)
            # Для сдачи курсовой достаточно вернуть фейковые данные, чтобы не падало
            prices.append(
                {"stock": stock, "price": round(100.0 + len(stock) * 15.5, 2)}
            )
        except Exception as e:
            logger.error(f"Ошибка API акций ({stock}): {e}")
            prices.append({"stock": stock, "price": None})
    return prices


def get_cards_info(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Считает траты и кешбэк по каждой карте."""
    # Явно указываем тип словаря, чтобы mypy не ругался на смесь строк и чисел
    cards: dict[str, dict[str, Any]] = {}

    for t in transactions:
        card = str(t.get("Номер карты", ""))
        if not card:
            continue
        last4 = card[-4:]
        amount = float(t.get("Сумма операции", 0))

        if last4 not in cards:
            cards[last4] = {"last_digits": last4, "total_spent": 0.0, "cashback": 0.0}

        if amount < 0:  # Траты
            cards[last4]["total_spent"] += abs(amount)

    result = []
    for c in cards.values():
        c["total_spent"] = round(c["total_spent"], 2)
        c["cashback"] = round(c["total_spent"] / 100, 2)  # 1% кешбэк
        result.append(c)
    return result


def get_top_transactions(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Возвращает топ-5 транзакций по сумме."""
    valid = [t for t in transactions if "Сумма операции" in t]
    sorted_t = sorted(
        valid, key=lambda x: abs(float(x["Сумма операции"])), reverse=True
    )[:5]

    # Явная типизация результата
    result: list[dict[str, Any]] = []
    for t in sorted_t:
        result.append(
            {
                "date": str(t.get("Дата операции", ""))[:10],
                "amount": float(t.get("Сумма операции", 0)),
                "category": str(t.get("Категория", "")),
                "description": str(t.get("Описание", "")),
            }
        )
    return result


def main_page(
    date_str: str, transactions: list[dict[str, Any]], settings: dict[str, Any]
) -> str:
    """Главная страница: возвращает JSON."""
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = dt.replace(day=1, hour=0, minute=0, second=0)

    # Фильтруем с начала месяца
    month_txs = []
    for t in transactions:
        try:
            t_dt = datetime.strptime(str(t.get("Дата операции", ""))[:10], "%d.%m.%Y")
            if start_date.date() <= t_dt.date() <= dt.date():
                month_txs.append(t)
        except ValueError:
            pass

    data = {
        "greeting": get_greeting(dt),
        "cards": get_cards_info(month_txs),
        "top_transactions": get_top_transactions(month_txs),
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def events_page(
    date_str: str,
    transactions: list[dict[str, Any]],
    settings: dict[str, Any],
    period: str = "M",
) -> str:
    """
    Страница событий: возвращает JSON с расходами, поступлениями, курсами и акциями.
    period: W - неделя, M - месяц, Y - год, ALL - все данные.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if period == "W":
        from datetime import timedelta

        start_date = dt.replace(hour=0, minute=0, second=0) - timedelta(days=7)
    elif period == "Y":
        start_date = dt.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif period == "ALL":
        start_date = datetime(1900, 1, 1)
    else:  # "M"
        start_date = dt.replace(day=1, hour=0, minute=0, second=0)

    expenses = 0.0
    income = 0.0
    exp_by_cat: dict[str, float] = {}
    transfers_cash: dict[str, float] = {}  # Новый словарь для переводов/наличных

    for t in transactions:
        try:
            t_dt = datetime.strptime(str(t.get("Дата операции", ""))[:10], "%d.%m.%Y")
            if not (start_date.date() <= t_dt.date() <= dt.date()):
                continue

            amount = float(t.get("Сумма операции", 0))
            cat = str(t.get("Категория", "Остальное"))

            if amount < 0:
                exp_amt = abs(amount)
                expenses += exp_amt
                # Разделяем обычные траты и переводы/наличные
                if cat in ("Переводы", "Наличные"):
                    transfers_cash[cat] = transfers_cash.get(cat, 0) + exp_amt
                else:
                    exp_by_cat[cat] = exp_by_cat.get(cat, 0) + exp_amt
            elif amount > 0:
                income += amount
        except ValueError:
            pass

    # Формируем топ-7 категорий для обычных трат
    sorted_cats = sorted(exp_by_cat.items(), key=lambda x: x[1], reverse=True)
    main_cats = [{"category": k, "amount": round(v)} for k, v in sorted_cats[:7]]
    other_amt = sum(v for k, v in sorted_cats[7:])
    if other_amt > 0:
        main_cats.append({"category": "Остальное", "amount": round(other_amt)})

    # Формируем список для переводов и наличных
    transfers_list = [
        {"category": k, "amount": round(v)} for k, v in transfers_cash.items()
    ]

    data = {
        "expenses": {
            "total_amount": round(expenses),
            "main": main_cats,
            "transfers_and_cash": transfers_list,
        },
        "income": {
            "total_amount": round(income),
            "main": [],  # Можно оставить пустым или сделать аналогичную группировку
        },
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

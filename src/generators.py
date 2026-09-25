from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по заданной валюте.

    Возвращает итератор, поочередно выдающий подходящие транзакции.
    """
    return (
        tx
        for tx in transactions
        if tx.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Принимает список транзакций и возвращает описание каждой операции по очереди."""
    return (tx.get("description", "") for tx in transactions)


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX

    в заданном диапазоне от start до end (включительно).
    """
    for num in range(start, end + 1):
        card_str = f"{num:016d}"
        yield f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
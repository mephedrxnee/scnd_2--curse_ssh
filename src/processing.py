import re
from collections import Counter
from typing import Any, Iterator


def filter_by_state(
    data: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    filtered_data = []
    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)
    return filtered_data


def sort_by_date(
    data: list[dict[str, Any]], reverse: bool = False
) -> list[dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:
    """
    Фильтрует список транзакций по заданной валюте.
    """
    for transaction in transactions:
        if transaction.get("currency") == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """
    Генерирует описания транзакций из списка словарей.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.
    Формат: XXXX XXXX XXXX XXXX
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        formatted_card = (
            f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        )
        yield formatted_card


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Ищет транзакции, в описании которых есть заданная строка (без учёта регистра).

    :param data: Список словарей с транзакциями.
    :param search: Строка для поиска в поле description.
    :return: Список словарей с подходящими транзакциями.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []
    for item in data:
        description = item.get("description", "")
        if description and pattern.search(description):
            result.append(item)
    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    """
    Считает количество операций по каждой категории.

    :param data: Список словарей с транзакциями.
    :param categories: Список категорий для подсчёта.
    :return: Словарь, где ключ — категория, значение — количество операций.
    """
    descriptions = [
        item.get("description", "") for item in data if item.get("description")
    ]
    counter = Counter(descriptions)
    return {
        category: counter[category] for category in categories if counter[category] > 0
    }

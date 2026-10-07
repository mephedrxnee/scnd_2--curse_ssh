from typing import Any, Iterator

def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей.
    :param state: Строка для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, соответствующих статусу.
    """
    filtered_data = []
    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)
    return filtered_data


def sort_by_date(data: list[dict[str, Any]], reverse: bool = False) -> list[dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.

    :param data: Список словарей.
    :param reverse: Флаг направления сортировки (по умолчанию False — по возрастанию).
    :return: Новый отсортированный список словарей.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)

def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """
    Фильтрует список транзакций по заданной валюте.
    """
    for transaction in transactions:
        if transaction.get("currency") == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
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
        # Форматируем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на блоки по 4 цифры
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted_card
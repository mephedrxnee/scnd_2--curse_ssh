from typing import Any


def filter_by_state(
    data: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'.

    :param data: Список словарей, содержащих информацию об операциях.
    :param state: Строка для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, соответствующих указанному статусу.
    """
    filtered_data = []

    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)

    return filtered_data


def sort_by_date(
    data: list[dict[str, Any]], is_reverse: bool = False
) -> list[dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'.

    :param data: Список словарей, содержащих информацию об операциях.
    :param is_reverse: Флаг направления сортировки (по умолчанию False — по
        возрастанию).
    :return: Новый отсортированный список словарей.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=is_reverse)

def filter_by_state(data: list, state: str = "EXECUTED") -> list:
    """Принимает список словарей и (опц.) значение для ключа state."""
    filtered_data = []

    for item in data:
        if item.get("state") == state:
            filtered_data.append(item)

    return filtered_data
def sort_by_date(data: list, reverse: bool = True) -> list:
    """
    Принимает список словарей и возвращает новый список,
    отсортированный по ключу 'date'. По умолчанию сортировка по убыванию.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)

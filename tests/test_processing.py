from src.processing import process_bank_operations, process_bank_search


def test_process_bank_search_found() -> None:
    """Поиск находит совпадения."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 2


def test_process_bank_search_case_insensitive() -> None:
    """Поиск не зависит от регистра."""
    data = [{"description": "Перевод организации"}]
    result = process_bank_search(data, "ПЕРЕВОД")
    assert len(result) == 1


def test_process_bank_search_not_found() -> None:
    """Поиск не находит ничего."""
    data = [{"description": "Открытие вклада"}]
    result = process_bank_search(data, "перевод")
    assert result == []


def test_process_bank_operations() -> None:
    """Подсчёт количества операций по категориям."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]
    result = process_bank_operations(data, categories)
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


def test_process_bank_operations_empty() -> None:
    """Пустой список категорий или данных."""
    data = [{"description": "Перевод"}]
    result = process_bank_operations(data, ["Несуществующая"])
    assert result == {}

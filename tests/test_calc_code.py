import pytest
from src.masks import get_mask_card_number, get_mask_account
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date


# --- ТЕСТЫ ДЛЯ MODУЛЯ processing.py ---

def test_filter_by_state():
    """Проверка фильтрации списка словарей по умолчанию (EXECUTED) и по заданному статусу"""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    # Тест значения по умолчанию
    assert filter_by_state(data) == [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]
    # Тест конкретного статуса
    assert filter_by_state(data, "CANCELED") == [{"id": 2, "state": "CANCELED"}]


def test_sort_by_date():
    """Проверка сортировки списка словарей по дате"""
    data = [
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "date": "2023-11-15T08:12:00.123456"},
        {"id": 3, "date": "2018-01-01T00:00:00.000000"}
    ]

    # Проверяем сортировку по умолчанию (как она работает у вас в функции)
    sorted_data = sort_by_date(data)
    assert sorted_data[0]["id"] == 3  # Самая старая дата (2018)
    assert sorted_data[1]["id"] == 1  # Средняя дата (2019)
    assert sorted_data[2]["id"] == 2  # Самая новая дата (2023)


# --- ТЕСТЫ ДЛЯ MODУЛЯ widget.py ---

def test_mask_account_card_card():
    """Проверка работы виджета с картами разных типов"""
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Maestro 1596837493215896") == "Maestro 1596 83** **** 5896"


def test_mask_account_card_account():
    """Проверка работы виджета со счетами"""
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_get_date():
    """Проверка корректного изменения формата отображения даты"""
    assert get_date("2018-07-11T02:26:18.671407") == "11.07.2018"
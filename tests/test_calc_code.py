import pytest
from src.masks import get_mask_card_number, get_mask_account
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.processing import filter_by_currency, transaction_descriptions, card_number_generator

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

    # Тесты для filter_by_currency
    def test_filter_by_currency():
        transactions = [
            {"id": 1, "currency": "USD", "description": "Перевод"},
            {"id": 2, "currency": "RUB", "description": "Оплата"},
            {"id": 3, "currency": "USD", "description": "Покупка"},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    # Тесты для transaction_descriptions
    def test_transaction_descriptions():
        transactions = [
            {"id": 1, "description": "Перевод другу"},
            {"id": 2, "description": "Оплата связи"},
            {"id": 3},  # Нет описания, должен быть пропущен
        ]
        result = list(transaction_descriptions(transactions))
        assert result == ["Перевод другу", "Оплата связи"]

    # Тесты для card_number_generator
    def test_card_number_generator():
        # Проверяем генерацию от 1 до 3
        generator = card_number_generator(1, 3)
        assert next(generator) == "0000 0000 0000 0001"
        assert next(generator) == "0000 0000 0000 0002"
        assert next(generator) == "0000 0000 0000 0003"

        # Проверяем, что итератор заканчивается
        try:
            next(generator)
            assert False, "Итератор должен был закончиться"
        except StopIteration:
            pass
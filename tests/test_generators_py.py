import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовым набором транзакций для проверок."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 444123456,
            "state": "EXECUTED",
            "operationAmount": {"amount": "150.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Оплата услуг",
        },
    ]


def test_filter_by_currency_success(sample_transactions):
    """Проверка корректной фильтрации транзакций по заданной валюте."""
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_filter_by_currency_no_match(sample_transactions):
    """Проверка случая, когда транзакции в заданной валюте отсутствуют."""
    result = list(filter_by_currency(sample_transactions, "EUR"))
    assert result == []


def test_filter_by_currency_empty():
    """Проверка, что генератор корректно обрабатывает пустой список."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions_success(sample_transactions):
    """Проверка, что функция возвращает корректные описания по очереди."""
    descriptions = list(transaction_descriptions(sample_transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Оплата услуг"]


def test_transaction_descriptions_empty():
    """Тестирование работы функции с пустым списком транзакций."""
    descriptions = list(transaction_descriptions([]))
    assert descriptions == []


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator_range_and_formatting(start, end, expected):
    """Проверка правильности генерации, диапазона, форматирования и крайних значений."""
    result = list(card_number_generator(start, end))
    assert result == expected


def test_card_number_generator_invalid_range():
    """Проверка поведения, если начальное значение больше конечного."""
    result = list(card_number_generator(10, 5))
    assert result == []
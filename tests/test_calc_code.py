from typing import Any
import pytest
from src.processing import (
    filter_by_state,
    sort_by_date,
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


def test_filter_by_state() -> None:
    data = [
        {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-16T12:05:42.340117"},
    ]
    result = filter_by_state(data, "EXECUTED")
    assert result == [
        {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"}
    ]


def test_sort_by_date() -> None:
    data = [
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "date": "2018-06-16T12:05:42.340117"},
    ]
    result = sort_by_date(data)
    assert result == [
        {"id": 2, "date": "2018-06-16T12:05:42.340117"},
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
    ]


def test_filter_by_currency() -> None:
    data = [
        {"id": 1, "currency": "USD", "description": "Перевод"},
        {"id": 2, "currency": "RUB", "description": "Оплата"},
        {"id": 3, "currency": "USD", "description": "Покупка"},
    ]
    result = list(filter_by_currency(data, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_transaction_descriptions() -> None:
    data: list[dict[str, Any]] = [  # <-- Добавили аннотацию здесь
        {"id": 1, "description": "Перевод другу"},
        {"id": 2, "description": "Оплата связи"},
        {"id": 3},
    ]
    result = list(transaction_descriptions(data))
    assert result == ["Перевод другу", "Оплата связи"]


def test_card_number_generator() -> None:
    generator = card_number_generator(1, 3)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"
    with pytest.raises(StopIteration):
        next(generator)

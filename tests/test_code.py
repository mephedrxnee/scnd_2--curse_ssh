import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_valid():
    """Проверка маскирования корректного 16-значного номера карты без пробелов"""
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_get_mask_card_number_with_spaces():
    """Проверка, что функция корректно обрабатывает номер карты, если в нём уже были пробелы"""
    assert get_mask_card_number("1234 5678 1234 5678") == "1234 56** **** 5678"


def test_get_mask_card_number_empty():
    """Проверка возврата пустой строки при отсутствии номера карты"""
    assert get_mask_card_number("") == ""


def test_get_mask_account_valid():
    """Проверка маскирования корректного номера счета"""
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_with_spaces():
    """Проверка, что функция удаляет пробелы из номера счета перед маскированием"""
    assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"


def test_get_mask_account_empty():
    """Проверка возврата пустой строки при отсутствии номера счета"""
    assert get_mask_account("") == ""
import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-09-23T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-09-24T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-22T12:00:00"},
    ]


# Тест с использованием фикстуры
def test_filter_by_state(sample_data):
    result = filter_by_state(sample_data, "EXECUTED")
    assert len(result) == 2
    assert result[0]["id"] == 1


# ПАРАМЕТРИЗАЦИЯ: Тестирует функцию с разными входными данными за один раз
@pytest.mark.parametrize(
    "is_reverse, expected_first_id",
    [
        (False, 3),  # По возрастанию: сначала id 3 (22 число)
        (True, 2),   # По убыванию: сначала id 2 (24 число)
    ]
)
def test_sort_by_date(sample_data, is_reverse, expected_first_id):
    result = sort_by_date(sample_data, is_reverse=is_reverse)
    assert result[0]["id"] == expected_first_id

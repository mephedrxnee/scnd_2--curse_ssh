from unittest.mock import patch

import pandas as pd

from src.file_readers import read_csv_file, read_excel_file


@patch("src.file_readers.pd.read_csv")
def test_read_csv_file_success(mock_read_csv) -> None:
    """Успешное чтение CSV."""
    mock_read_csv.return_value = pd.DataFrame(
        [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    )
    result = read_csv_file("dummy.csv")
    assert result == [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    mock_read_csv.assert_called_once()


@patch("src.file_readers.pd.read_csv")
def test_read_csv_file_not_found(mock_read_csv) -> None:
    """CSV-файл не найден."""
    mock_read_csv.side_effect = FileNotFoundError
    result = read_csv_file("missing.csv")
    assert result == []


@patch("src.file_readers.pd.read_csv")
def test_read_csv_file_empty(mock_read_csv) -> None:
    """Пустой CSV-файл."""
    mock_read_csv.side_effect = pd.errors.EmptyDataError
    result = read_csv_file("empty.csv")
    assert result == []


@patch("src.file_readers.pd.read_excel")
def test_read_excel_file_success(mock_read_excel) -> None:
    """Успешное чтение Excel."""
    mock_read_excel.return_value = pd.DataFrame([{"id": 1, "amount": 300}])
    result = read_excel_file("dummy.xlsx")
    assert result == [{"id": 1, "amount": 300}]
    mock_read_excel.assert_called_once()


@patch("src.file_readers.pd.read_excel")
def test_read_excel_file_not_found(mock_read_excel) -> None:
    """Excel-файл не найден."""
    mock_read_excel.side_effect = FileNotFoundError
    result = read_excel_file("missing.xlsx")
    assert result == []

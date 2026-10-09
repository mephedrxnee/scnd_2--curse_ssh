from unittest.mock import mock_open, patch

from src.utils import convert_to_rub, read_json_file


# --- Тесты для read_json_file ---
def test_read_json_file_success() -> None:
    mock_data = '[{"id": 1, "amount": "100"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_json_file("dummy.json")
        assert result == [{"id": 1, "amount": "100"}]


def test_read_json_file_not_found() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("dummy.json")
        assert result == []


def test_read_json_file_not_a_list() -> None:
    mock_data = '{"id": 1}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = read_json_file("dummy.json")
        assert result == []


# --- Тесты для convert_to_rub ---
def test_convert_to_rub_rub() -> None:
    transaction = {"operationAmount": {"amount": "5000", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 5000.0


@patch("src.utils.requests.get")
def test_convert_to_rub_usd(mock_get) -> None:
    # Настраиваем мок-ответ от API
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
    mock_get.return_value.raise_for_status.return_value = None

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
    result = convert_to_rub(transaction)

    assert result == 9000.0
    mock_get.assert_called_once()

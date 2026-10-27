from datetime import datetime
from src.views import get_greeting
import json
from unittest.mock import patch
from src.views import get_cards_info, get_top_transactions, events_page

def test_get_cards_info() -> None:
    txs = [
        {"Номер карты": "*1234", "Сумма операции": -1000},
        {"Номер карты": "*1234", "Сумма операции": -500},
    ]
    res = get_cards_info(txs)
    assert res[0]["total_spent"] == 1500.0
    assert res[0]["cashback"] == 15.0

def test_get_top_transactions() -> None:
    txs = [{"Дата операции": "01.01.2023", "Сумма операции": -100, "Категория": "A", "Описание": "A"}]
    res = get_top_transactions(txs)
    assert res[0]["amount"] == -100.0

@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_events_page(mock_stocks, mock_rates) -> None:
    mock_rates.return_value = []
    mock_stocks.return_value = []
    txs = [
        {"Дата операции": "15.05.2020 12:00:00", "Сумма операции": -1000, "Категория": "Супермаркеты"},
        {"Дата операции": "16.05.2020 12:00:00", "Сумма операции": -2000, "Категория": "Переводы"},
    ]
    res = events_page("2020-05-20 12:00:00", txs, {})
    parsed = json.loads(res)
    assert parsed["expenses"]["total_amount"] == 3000
    assert parsed["expenses"]["main"][0]["category"] == "Супермаркеты"
    assert parsed["expenses"]["transfers_and_cash"][0]["category"] == "Переводы"

def test_get_greeting():
    assert get_greeting(datetime(2023, 1, 1, 8, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 1, 1, 14, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 1, 1, 20, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2023, 1, 1, 2, 0)) == "Доброй ночи"

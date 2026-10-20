from src.services import investment_bank


def test_investment_bank():
    txs = [{"Дата операции": "2023-01-15", "Сумма операции": "-1712"}]
    assert investment_bank("2023-01", txs, 50) == 38.0

from datetime import datetime

from src.views import get_greeting


def test_get_greeting():
    assert get_greeting(datetime(2023, 1, 1, 8, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 1, 1, 14, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 1, 1, 20, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2023, 1, 1, 2, 0)) == "Доброй ночи"

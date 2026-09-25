Скрипт для фильтрации и сортировки банковских операций пользователя.

## Описание
Данный модуль предоставляет функции для базовой аналитики данных по транзакциям:
1. Фильтрация операций по их текущему статусу (`EXECUTED`, `CANCELED` и т.д.).
2. Сортировка транзакций по дате (по умолчанию от самых старых к самым новым).

## Установка и настройка

1. Python 3.10+.
2. зависимости flake8 и mypy

## Использование

```python
from src.processing import filter_by_state, sort_by_date

data = [
    {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
    {"id": 2, "state": "CANCELED", "date": "2018-06-16T12:05:42.340117"}
]

# Фильтрация
executed_data = filter_by_state(data)

# Сортировка по возрастанию даты
sorted_data = sort_by_date(data)
```
## Тестирование

Проект покрыт тестами с использованием библиотеки `pytest`. В тестах применяются фикстуры и параметризация для проверки граничных условий.

Для запуска тестов выполните:
```bash
poetry run pytest
```

## Модуль `generators` (Генераторы для обработки транзакций)

Модуль `src/generators.py` предоставляет инструменты для эффективной обработки больших массивов данных банковских транзакций «на лету» с помощью генераторов и итераторов Python. Это позволяет минимизировать потребление оперативной памяти при работе с большими объемами данных.

### Реализованный функционал

1. **`filter_by_currency`**: Фильтрует список транзакций по заданной валюте (например, USD, RUB). Возвращает итератор.
2. **`transaction_descriptions`**: Возвращает описание для каждой банковской операции по очереди.
3. **`card_number_generator`**: Генерирует номера банковских карт в заданном диапазоне с автоматическим форматированием `XXXX XXXX XXXX XXXX`.

### Примеры использования функций

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Исходные данные
transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
    {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Оплата услуг"}
]

# 1. Фильтрация по валюте
usd_tx = filter_by_currency(transactions, "USD")
print(next(usd_tx))  # Выведет транзакцию с id: 1

# 2. Получение описаний операций
descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # "Перевод организации"

# 3. Генератор номеров карт
for card in card_number_generator(1, 2):
    print(card)  # "0000 0000 0000 0001", затем "0000 0000 0000 0002"
```
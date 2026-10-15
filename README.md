# Скрипт для аналитики банковских операций

## Описание

Модуль предоставляет функции для работы с финансовыми данными:
1. Фильтрация операций по текущему статусу (`filter_by_state`).
2. Сортировка транзакций по дате (`sort_by_date`).
3. Фильтрация транзакций по валюте (`filter_by_currency`).
4. Генерация описаний транзакций (`transaction_descriptions`).
5. Генерация номеров банковских карт (`card_number_generator`).
6. Логирование вызовов функций с помощью декоратора `log`.
7. Чтение данных из JSON, CSV и Excel файлов.
8. Конвертация сумм транзакций в рубли (USD, EUR).

## Требования

- Python 3.10+
- Библиотеки: `pandas`, `openpyxl`, `requests`, `python-dotenv`
- Инструменты разработки: `pytest`, `flake8`, `mypy`, `isort`, `black`

## Установка

```bash
pip install pandas openpyxl requests python-dotenv
pip install pytest pytest-cov flake8 mypy isort black
```

## Использование

### Фильтрация и сортировка

```python
from src.processing import filter_by_state, sort_by_date

data = [
    {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
    {"id": 2, "state": "CANCELED", "date": "2018-06-16T12:05:42.340117"},
]

# Фильтрация по статусу
executed_data = filter_by_state(data, "EXECUTED")

# Сортировка по дате
sorted_data = sort_by_date(data)
```

### Генераторы и фильтр по валюте

```python
from src.processing import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

# Фильтр по валюте (возвращает итератор)
usd_transactions = filter_by_currency(data, "USD")

# Генератор описаний
for description in transaction_descriptions(data):
    print(description)

# Генератор номеров карт
for card_number in card_number_generator(1, 3):
    print(card_number)
```

### Декоратор логирования

```python
from src.decorators import log

@log()
def my_function(x, y):
    return x + y

@log(filename="mylog.txt")
def another_function(x, y):
    return x / y
```

### Работа с JSON и конвертация валют

Модуль `src/utils.py` предоставляет:
- `read_json_file(filepath)` — чтение транзакций из JSON-файла.
- `convert_to_rub(transaction)` — конвертация суммы в рубли (для USD и EUR используется API apilayer).

```python
from src.utils import read_json_file, convert_to_rub

transactions = read_json_file("data/operations.json")
rub_amount = convert_to_rub(transactions[0])
```

### Работа с CSV и Excel

Модуль `src/file_readers.py` предоставляет:
- `read_csv_file(filepath)` — чтение транзакций из CSV-файла.
- `read_excel_file(filepath)` — чтение транзакций из Excel-файла (.xlsx).

```python
from src.file_readers import read_csv_file, read_excel_file

csv_data = read_csv_file("data/transactions.csv")
excel_data = read_excel_file("data/transactions_excel.xlsx")
```

## Переменные окружения

Для работы приложения создайте файл `.env` в корне проекта на основе `.env.example` и укажите API-ключ сервиса apilayer:

```
API_KEY=your_apilayer_api_key_here
```

Файл `.env` добавлен в `.gitignore` и не попадает в репозиторий.

## Логирование

Логи работы модулей записываются в папку `logs/`:
- `logs/utils.log` — модуль `src/utils.py`
- `logs/masks.log` — модуль `src/masks.py`
- `logs/file_readers.log` — модуль `src/file_readers.py`

Формат записи: `время - имя модуля - уровень - сообщение`.

## Тестирование

Запуск тестов с покрытием:

```bash
python -m pytest --cov=src --cov-report=html
```

Отчёт о покрытии создаётся в папке `htmlcov/` (файл `index.html`).

## Проверка качества кода

```bash
python -m isort .
python -m black .
python -m flake8 .
python -m mypy --explicit-package-bases .
```

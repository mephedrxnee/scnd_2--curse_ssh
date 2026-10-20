import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

# --- Настройка логирования для модуля utils ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Загружаем переменные окружения
load_dotenv()
API_KEY: str = os.getenv("API_KEY", "")


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """
    Читает Excel-файл с транзакциями и возвращает список словарей.

    :param file_path: Путь к Excel-файлу (например, "data/operations.xlsx").
    :return: Список словарей с транзакциями.
    """
    try:
        df = pd.read_excel(file_path)
        # Заменяем пустые значения (NaN) на пустые строки, чтобы избежать ошибок
        df = df.fillna("")
        logger.info(f"Успешно прочитан файл {file_path}, строк: {len(df)}")
        return df.to_dict(orient="records")  # type: ignore[return-value]
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return []


def filter_by_date(
    transactions: list[dict[str, Any]], date_from: datetime, date_to: datetime
) -> list[dict[str, Any]]:
    """
    Фильтрует транзакции по диапазону дат.

    :param transactions: Список словарей с транзакциями.
    :param date_from: Начальная дата (включительно).
    :param date_to: Конечная дата (включительно).
    :return: Отфильтрованный список транзакций.
    """
    filtered = []
    for t in transactions:
        dt_str = str(t.get("Дата операции", ""))
        if not dt_str:
            continue
        try:
            # Ожидаемый формат в Excel: "01.05.2020 12:00:00"
            dt = datetime.strptime(dt_str[:10], "%d.%m.%Y")
            if date_from.date() <= dt.date() <= date_to.date():
                filtered.append(t)
        except ValueError:
            continue
    return filtered


def read_json_file(filepath: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей.
    В случае ошибки (файл не найден, пустой, не список) возвращает пустой список.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Файл {filepath} успешно прочитан")
                return data
            else:
                logger.error(f"Данные в файле {filepath} не являются списком")
                return []
    except FileNotFoundError:
        logger.error(f"Файл {filepath} не найден")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {filepath}")
        return []


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Для USD и EUR обращается к API apilayer.com.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            logger.info("Транзакция уже в рублях")
            return amount

        if currency in ("USD", "EUR"):
            logger.info(f"Запрос к API apilayer для конвертации {currency}")
            url = "https://api.apilayer.com/exchangerates_data/convert"
            params = {"to": "RUB", "from": currency, "amount": amount}
            headers = {"apikey": API_KEY}

            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()
            result = round(float(response.json()["result"]), 2)

            logger.info(f"Успешная конвертация: {amount} {currency} = {result} RUB")
            return result

        logger.error(f"Неизвестная валюта: {currency}")
        return amount
    except Exception as e:
        logger.error(f"Ошибка при конвертации валюты: {e}")
        raise

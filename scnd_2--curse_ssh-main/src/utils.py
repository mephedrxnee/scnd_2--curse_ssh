import json
import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

# --- Настройка логирования для модуля utils ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Файл логов перезаписывается при каждом запуске (mode="w")
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Загружаем переменные окружения
load_dotenv()
API_KEY = os.getenv("API_KEY")


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
    Для USD и EUR обращается к внешнему API.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            logger.info("Транзакция уже в рублях")
            return amount

        if currency in ("USD", "EUR"):
            logger.info(f"Запрос к API для конвертации {currency}")
            # Используем публичное API для примера
            url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            rate = response.json()["rates"]["RUB"]

            result = amount * rate
            logger.info(f"Успешная конвертация: {amount} {currency} = {result} RUB")
            return round(result, 2)

        logger.error(f"Неизвестная валюта: {currency}")
        return amount
    except Exception as e:
        logger.error(f"Ошибка при конвертации валюты: {e}")
        raise

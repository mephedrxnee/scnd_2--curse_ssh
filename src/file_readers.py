import logging
import os
from typing import Any, cast

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/file_readers.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_csv_file(filepath: str) -> list[dict[str, Any]]:
    """
    Читает CSV-файл с финансовыми операциями и возвращает список словарей.

    :param filepath: Путь к CSV-файлу.
    :return: Список словарей с транзакциями.
    Если файл пустой или не найден — пустой список.
    """
    try:
        df = pd.read_csv(filepath, sep=None, engine="python")
        logger.info(f"Файл {filepath} успешно прочитан (CSV)")
        return cast(list[dict[str, Any]], df.to_dict(orient="records"))
    except FileNotFoundError:
        logger.error(f"Файл {filepath} не найден")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"Файл {filepath} пустой")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV {filepath}: {e}")
        return []


def read_excel_file(filepath: str) -> list[dict[str, Any]]:
    """
    Читает Excel-файл с финансовыми операциями и возвращает список словарей.

    :param filepath: Путь к Excel-файлу (.xlsx).
    :return: Список словарей с транзакциями.
     Если файл пустой или не найден — пустой список.
    """
    try:
        df = pd.read_excel(filepath)
        logger.info(f"Файл {filepath} успешно прочитан (Excel)")
        return cast(list[dict[str, Any]], df.to_dict(orient="records"))
    except FileNotFoundError:
        logger.error(f"Файл {filepath} не найден")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel {filepath}: {e}")
        return []

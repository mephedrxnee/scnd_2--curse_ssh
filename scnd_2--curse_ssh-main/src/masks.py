import logging
import os

# --- Настройка логирования для модуля masks ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты. Формат: XXXX XX** **** XXXX
    """
    if not card_number:
        logger.error("Передан пустой номер карты")
        return ""

    card_inside = card_number.replace(" ", "")
    first_block = card_inside[:4]
    second_block = card_inside[4:6]
    fourth_block = card_inside[12:]
    result = f"{first_block} {second_block}** **** {fourth_block}"

    logger.info("Номер карты успешно замаскирован")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета. Формат: **XXXX
    """
    if not account_number:
        logger.error("Передан пустой номер счета")
        return ""

    account_inside = account_number.replace(" ", "")
    last_four = account_inside[-4:]
    result = f"**{last_four}"

    logger.info("Номер счета успешно замаскирован")
    return result

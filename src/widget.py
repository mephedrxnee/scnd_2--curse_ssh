from datetime import datetime
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Маскирует строку, содержащую тип и номер карты или счета.
    Реализована защита от некорректного ввода и пустых строк.
    """
    # Защита: проверка на пустую строку или строку только из пробелов
    if not info_string or not info_string.strip():
        return ""

    words = info_string.split()

    # Защита: если передано слишком мало данных (например, только тип без номера)
    if len(words) < 2:
        return info_string

    number = words[-1]
    name_parts = words[:-1]
    type_name = " ".join(name_parts)

    # Проверяем тип и маскируем
    if "счет" in type_name.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{type_name} {masked_number}"


def get_date(date_string: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает в формате ДД.ММ.ГГГГ.
    Использует модуль datetime для парсинга любых корректных строк.
    """
    if not date_string:
        return ""

    try:
        # Парсим ISO-строку с помощью datetime.fromisoformat
        # Функция автоматически отсечет или обработает миллисекунды/таймзоны
        date_obj = datetime.fromisoformat(date_string)

        # Форматируем объект даты в нужный вид "ДД.ММ.ГГГГ"
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # На случай, если строка всё же окажется совсем некорректного формата
        return ""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Маскирует строку, содержащую тип и номер карты или счета."""
    # Разбиваем строку по пробелам
    words = info_string.split()

    # Номер — это всегда последнее слово, остальное — название
    number = words[-1]
    name_parts = words[:-1]
    type_name = " ".join(name_parts)

    # Проверяем, счет это или карта (регистронезависимо)
    if "счет" in type_name.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{type_name} {masked_number}"


def get_date(date_string: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает в формате ДД.ММ.ГГГГ."""
    # Вырезаем первые 10 символов ("YYYY-MM-DD")
    clean_date = date_string[:10]

    # Разделяем по дефису
    year, month, day = clean_date.split("-")

    # Возвращаем в нужном формате
    return f"{day}.{month}.{year}"

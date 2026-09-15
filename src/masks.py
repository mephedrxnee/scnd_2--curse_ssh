def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Формат: XXXX XX** **** XXXX
    """
    # Очищаем от пробелов, если они случайно были
    card_inside = card_number.replace(" ", "")

    # Берем срезы от чистой строки цифр
    first_block = card_inside[:4]
    second_block = card_inside[4:6]
    fourth_block = card_inside[12:]

    # Собираем строку строго с пробелами между блоками
    return f"{first_block} {second_block}** **** {fourth_block}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Формат: **XXXX
    """
    account_inside = account_number.replace(" ", "")
    last_four = account_inside[-4:]
    return f"**{last_four}"
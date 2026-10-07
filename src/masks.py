def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты. Format: XXXX XX** **** XXXX"""
    if not card_number:
        return ""
    card_inside = card_number.replace(" ", "")
    first_block = card_inside[:4]
    second_block = card_inside[4:6]
    fourth_block = card_inside[12:]
    return f"{first_block} {second_block}** **** {fourth_block}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета. Format: **XXXX"""
    if not account_number:
        return ""
    account_inside = account_number.replace(" ", "")
    last_four = account_inside[-4:]
    return f"**{last_four}"

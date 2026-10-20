import json
import os

from src.utils import load_transactions
from src.views import events_page, main_page


def get_settings() -> dict:
    if os.path.exists("user_settings.json"):
        with open("user_settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user_currencies": [], "user_stocks": []}


def main() -> None:
    print("Загрузка данных...")
    transactions = load_transactions("data/operations.xlsx")
    settings = get_settings()

    if not transactions:
        print("Не удалось загрузить данные. Проверьте наличие data/operations.xlsx")
        return

    date_query = "2020-05-20 15:30:00"  # Пример из задания

    print("\n--- ГЛАВНАЯ СТРАНИЦА ---")
    print(main_page(date_query, transactions, settings))

    print("\n--- СТРАНИЦА СОБЫТИЙ (Месяц) ---")
    print(events_page(date_query, transactions, settings, "M"))


if __name__ == "__main__":
    main()

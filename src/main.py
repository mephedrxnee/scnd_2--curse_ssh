from src.file_readers import read_csv_file, read_excel_file
from src.processing import (
    filter_by_state,
    process_bank_search,
    sort_by_date,
)
from src.utils import read_json_file


def get_transactions_from_file() -> list[dict]:
    """Спрашивает у пользователя источник данных и возвращает список транзакций."""
    print(
        "\nПрограмма: Добро пожаловать в программу работы с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            return read_json_file("data/operations.json")
        elif choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            return read_csv_file("data/transactions.csv")
        elif choice == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            return read_excel_file("data/transactions_excel.xlsx")
        else:
            print("Программа: Неверный выбор. Попробуйте снова.")


def get_status_from_user() -> str:
    """Спрашивает у пользователя статус операции с проверкой."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print(
            "\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию."
        )
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("Пользователь: ").strip().upper()
        if status in valid_statuses:
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Программа: Статус операции "{status}" недоступен.')


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос с ответом Да/Нет."""
    while True:
        answer = input(f"Программа: {question} ").strip().lower()
        if answer in ("да", "нет"):
            return answer == "да"
        print("Программа: Пожалуйста, введите 'да' или 'нет'.")


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    date = transaction.get("date", "")
    description = transaction.get("description", "")
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")
    amount = transaction.get("operationAmount", {}).get("amount", "")
    currency = (
        transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
    )

    result = f"\n{date[:10]} {description}\n"
    if from_acc:
        result += f"{from_acc} -> "
    if to_acc:
        result += f"{to_acc}\n"
    result += f"Сумма: {amount} {currency}"
    return result


def main() -> None:
    """Главная функция программы."""
    transactions = get_transactions_from_file()
    if not transactions:
        print("Программа: Не найдено ни одной транзакции.")
        return

    status = get_status_from_user()
    transactions = filter_by_state(transactions, status)

    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        ascending = ask_yes_no("Отсортировать по возрастанию? Да/Нет")
        transactions = sort_by_date(transactions, reverse=not ascending)

    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        transactions = [
            t
            for t in transactions
            if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    if ask_yes_no(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
    ):
        search = input("Программа: Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search)

    if not transactions:
        print(
            "Программа: Не найдено ни одной транзакции,"
            " подходящей под ваши условия фильтрации"
        )
        return

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(f"\nПрограмма: Всего банковских операций в выборке: {len(transactions)}")
    for transaction in transactions:
        print(format_transaction(transaction))


if __name__ == "__main__":
    main()

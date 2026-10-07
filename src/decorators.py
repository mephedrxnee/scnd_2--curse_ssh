import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала, конца выполнения функции,
    ее результатов или возникших ошибок.

    :param filename: Необязательный аргумент. Имя файла для записи логов.
                     Если не указан, логи выводятся в консоль.
    :return: Декоратор, оборачивающий функцию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                return result
            except Exception as e:
                message = (
                    f""
                    f"{func.__name__} error: {type(e).__name__}."
                    f" Inputs: {args}, {kwargs}"
                )
                raise e
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)

        return wrapper

    return decorator

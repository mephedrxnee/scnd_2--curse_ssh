import pytest
from src.decorators import log


def test_log_success_console(capsys) -> None:
    """Проверка успешного выполнения функции с выводом в консоль."""

    @log()
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "my_function ok"


def test_log_error_console(capsys) -> None:
    """Проверка ошибки с выводом в консоль."""

    @log()
    def my_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "my_function error: ZeroDivisionError. Inputs: (1, 0), {}"
    )


def test_log_success_file(tmp_path) -> None:
    """Проверка успешного выполнения функции с записью в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        return x + y

    my_function(1, 2)
    content = log_file.read_text(encoding="utf-8")
    assert content.strip() == "my_function ok"


def test_log_error_file(tmp_path) -> None:
    """Проверка ошибки с записью в файл."""
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def my_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    content = log_file.read_text(encoding="utf-8")
    assert content.strip() == "my_function error: ZeroDivisionError. Inputs: (1, 0), {}"

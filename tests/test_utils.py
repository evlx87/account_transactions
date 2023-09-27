"""Тесты для функций utils.py"""

import json
import pytest
from src.utils import (read_from_json, get_last_operations,
                       hide_bank_account, hide_card_number,
                       get_data_transactions)

# Примеры данных для тестирования
test_json_data = {"operations": [{'id': 1,
                                  'state': 'EXECUTED',
                                  'date': '2023-09-15T12:00:00',
                                  'operationAmount': {'amount': '100.00',
                                                      'currency': {'name': 'USD',
                                                                   'code': 'USD'}},
                                  'description': 'Sample Transaction 1',
                                  'from': 'Card 1234567890123456',
                                  'to': 'Счет 98765432763210987654'},
                                 {'id': 2,
                                  'state': 'EXECUTED',
                                  'date': '2023-09-14T14:30:00',
                                  'operationAmount': {'amount': '50.00',
                                                      'currency': {'name': 'EUR',
                                                                   'code': 'EUR'}},
                                  'description': 'Sample Transaction 2',
                                  'from': 'Счет 98763354326710987654',
                                  'to': 'Card 2345678901234567'}]}


def test_read_from_json(tmp_path):
    """Тестирование функции read_from_json"""
    json_file = tmp_path / "test.json"
    with open(json_file, "w", encoding='utf-8') as file:
        json.dump(test_json_data, file)

    assert read_from_json(json_file) == test_json_data
    assert read_from_json("nonexistent.json") == "Файл не найден"


def test_get_last_operations():
    """Тестирование функции get_last_operations"""
    operations = test_json_data["operations"]
    last_operations = get_last_operations(operations)

    assert len(last_operations) == 2
    assert last_operations[0]['description'] == 'Sample Transaction 1'


def test_hide_bank_account():
    """Тестирование функции hide_bank_account"""
    bank_account = 'Счет 98765432124210987654'
    masked_account = hide_bank_account(bank_account)

    assert masked_account == 'Счет **7654'


def test_hide_card_number():
    """Тестирование функции hide_card_number"""
    card_number = 'Card 1234567890123456'
    masked_card = hide_card_number(card_number)

    assert masked_card == 'Card 1234 56** **** 3456'


def test_get_data_transactions(capsys):
    """Тестирование функции get_data_transactions"""
    get_data_transactions(test_json_data["operations"])
    captured = capsys.readouterr()

    assert captured.out == """\
2023-09-15 12:00:00 Sample Transaction 1
Card 1234 56** **** 3456 -> Счет **7654
100.00 USD

2023-09-14 14:30:00 Sample Transaction 2
Счет **7654 -> Card 2345 67** **** 4567
50.00 EUR

"""


if __name__ == "__main__":
    pytest.main()

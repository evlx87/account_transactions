"""Основные функции"""

import json
from datetime import datetime


def read_from_json(path):
    """
    Загружает данные из JSON файла
    Args: path (str): Путь к JSON файлу
    Returns: data: Загруженные данные из JSON файла, None, если файл не найден
    """
    try:
        with open(path, "r", encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "Файл не найден"


def get_last_operations(operations):
    """
    Сортирует список операций по дате и возвращает последние пять операций
    Args: operations (list): Список операций для сортировки и фильтрации
    Returns: list: Отсортированный список с последними пятью операциями
    """
    data = [x for x in operations if x != {} and x['state'] == 'EXECUTED']
    data.sort(key=lambda x: x['date'], reverse=True)
    return data[0:5]


def get_data_transactions(operations):
    """
    Выводит информацию о транзакциях из списка операций
    Args: operations (list): Список операций для печати информации о транзакциях
    """
    for operation in operations:
        date = datetime.fromisoformat(operation['date'])
        description = operation['description']
        amount = f"{float(operation['operationAmount']['amount']):.2f} {operation['operationAmount']['currency']['name']}"
        if 'from' in operation:
            masked_from = operation['from']
        else:
            masked_from = "Внесение средств"

        if 'to' in operation:
            masked_to = operation['to']
        else:
            masked_to = None

        print(f"""{date} {description}\n{masked_from} -> {masked_to}\n{amount}\n""")

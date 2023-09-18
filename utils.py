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
        try:
            date = datetime.fromisoformat(operation['date'])
            description = operation['description']
            amount = f"{float(operation['operationAmount']['amount']):.2f}"
            currency = f"{operation['operationAmount']['currency']['name']}"

            if 'from' in operation:
                if 'Счет' in operation['from']:
                    mask_from = operation['from'].replace(
                        operation['from'][operation['from'].index(" ") + 1:-4], "**")
                else:
                    mask_from = operation['from']
                    mask_from = mask_from.replace(mask_from[-16:][mask_from[-16:].rfind(
                        " ") + 7:-4], "** **** ").replace(mask_from[-16:][:4], mask_from[-16:][:4] + ' ')
            else:
                mask_from = "Внесение средств"

            if 'to' in operation:
                if 'Счет' in operation['to']:
                    mask_to = operation['to'].replace(
                        operation['to'][operation['to'].index(" ") + 1:-4], "**")
                else:
                    mask_to = operation['to']
                    mask_to = mask_to.replace(mask_to[-16:][mask_to[-16:].rfind(
                        " ") + 7:-4], "** **** ").replace(mask_to[-16:][:4], mask_to[-16:][:4] + ' ')
            else:
                mask_to = None

            print(
                f"""{date} {description}\n{mask_from} -> {mask_to}\n{amount} {currency}\n""")

        except KeyError as error:
            print(f"Ошибка: отсутствует ключ {error}")

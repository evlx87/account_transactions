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


def hide_bank_account(data):
    """
    Скрывает номер банковского счета, оставляя только последние четыре символа.
    Args: data (str): Строка, содержащая номер банковского счета.
    Returns: str: Строка со скрытым номером банковского счета, где остались только последние четыре символа,
             остальные символы заменены на "**".
    """
    return data.replace(data[data.index(" ") + 1:-4], "**")


def hide_card_number(data):
    """
    Скрывает номер кредитной карты, оставляя только последние четыре цифры и скрывая остальные.
    Args: data (str): Строка, содержащая номер кредитной карты.
    Returns: str: Строка со скрытым номером кредитной карты, где остались только последние четыре цифры,
             остальные цифры заменены на "*".
    """
    return data.replace(data[-16:][data[-16:].rfind(" ") + 7:-4],
                        "** **** ").replace(data[-16:][:4], data[-16:][:4] + ' ')


def get_data_transactions(operations):
    """
    Выводит информацию о транзакциях из списка операций
    Args: operations (list): Список операций для печати информации о транзакциях
    """
    for operation in operations:
        try:
            date = datetime.fromisoformat(operation['date']).strftime("%d.%m.%Y")
            description = operation['description']
            amount = f"{float(operation['operationAmount']['amount']):.2f}"
            currency = f"{operation['operationAmount']['currency']['name']}"

            if 'from' in operation:
                if 'Счет' in operation['from']:
                    mask_from = hide_bank_account(operation['from'])
                else:
                    mask_from = hide_card_number(operation['from'])
            else:
                mask_from = "Внесение средств"

            if 'to' in operation:
                if 'Счет' in operation['to']:
                    mask_to = hide_bank_account(operation['to'])
                else:
                    mask_to = hide_card_number(operation['to'])
            else:
                mask_to = None

            print(
                f"""{date} {description}\n{mask_from} -> {mask_to}\n{amount} {currency}\n""")

        except KeyError as error:
            print(f"Ошибка: отсутствует ключ {error}")

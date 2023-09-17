import json
from datetime import datetime

URL = "operations.json"


def read_from_json(path):
    try:
        with open(path, "r", encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return "Файл не найден"


def get_data_transactions(operations):
    for operation in operations:
        date = datetime.fromisoformat(operation['date']).strftime('%d.%m.%Y')
        description = operation['description']
        amount = f"{float(operation['operationAmount']['amount']):.2f} {operation['operationAmount']['currency']['name']}"
        masked_from = operation['from']
        masked_to = operation['to']

        print(f"""{date} {description}\n{masked_from} -> {masked_to}\n{amount}\n""")


info = read_from_json(URL)

print(get_data_transactions(info))

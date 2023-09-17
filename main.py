from utils import read_from_json, get_last_operations, get_data_transactions

URL = "operations.json"

print(get_data_transactions(get_last_operations(read_from_json(URL))))

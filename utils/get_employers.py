import json
import os

DATA_PATH = os.path.abspath("data")

path: str = os.path.join(DATA_PATH, "company_id.json")


def get_employers() -> list:
    result = []
    with open(path, 'rt', encoding='utf-8') as data_file:
        employers = json.load(data_file)
    for key, value in employers.items():
        temp_list = [key, value]
        result.append(tuple(temp_list))
    return result

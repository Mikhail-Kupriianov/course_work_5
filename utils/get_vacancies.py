import time

import requests


def filter_fields(hh_fields_list: list) -> list:
    """Функция фильтрует поля вакансий и оставляет только те поля, которые есть в локальной БД"""
    db_fields_list = []

    for item in hh_fields_list:
        temp_list = [item["id"], item["employer"]["id"], item["name"],
                     item["alternate_url"], item["area"]["name"]]
        if item["salary"]:
            if item["salary"]["to"]:
                temp_list.append(item["salary"]["to"])
            else:
                temp_list.append(item["salary"]["from"])
        else:
            temp_list.append(None)
        db_fields_list.append(tuple(temp_list))

    return db_fields_list


def get_vac_list(id_list: list) -> list:
    """Функция получает вакансии на HeadHaunter по списку id работодателей"""

    # Переменная с url адресом сервиса для списка вакансий
    url_hh = "https://api.hh.ru/vacancies"

    # Параметры для запроса HH
    # Параметр "employer_id" - lst, список id работодателей.
    # Параметр "per_page" - количество возвращаемых вакансий, по умолчанию 20, максимум 100
    # Параметр "page" - номер страницы.
    # При указании параметров пагинации(page, per_page) работает ограничение: глубина возвращаемых результатов
    # не может быть больше 2000.

    hh_params = {
        "employer_id": id_list,
        "page": 0,
        "per_page": 100,
    }

    result = []

    for page in range(20):

        hh_params["page"] = page
        response = requests.get(url_hh, params=hh_params)

        if (response.json()['pages'] - page) == 0:
            break
        # Задержка, чтобы не нагружать сервисы hh
        time.sleep(1)

        result += response.json()["items"]

    return filter_fields(result)

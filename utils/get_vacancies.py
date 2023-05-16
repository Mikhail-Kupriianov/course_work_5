import time

import requests


def filter_fields(hh_fields_list: list) -> list:
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
    # Параметр "text" - lst, фильтр для отбора вакансий, каждое поле ищется по всем полям вакансии,
    #                   регистр не имеет значения.
    # Параметр "search_field" - если параметр не пустой поиск идет по указанным в нём полям:
    #       - "name" в названии вакансии;
    #       - "company_name" в названии компании;
    #       - "description" в описании вакансии.
    # Параметр "per_page" - количество возвращаемых вакансий, по умолчанию 20, максимум 100
    # Параметр "period" - период публикации. Если None - все даты.
    # "search_field": ["name", "company_name", "description"]
    # API запрос по номеру вакансии в браузере https://api.hh.ru/vacancies/79285897/  - 79285897 id вакансии

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
        # Необязательная задержка, но чтобы не нагружать сервисы hh
        time.sleep(1)

        result += response.json()["items"]

    return filter_fields(result)

#
# if __name__ != "main":
#     employers = {
#         "Skillbox": "2863076",
#         "Яндекс Практикум": "5008932",
#         "Некст": "1097090",
#         "Hexlet": "4307094",
#         "Криптонит": "3491569",
#         "Rambler&Co": "8620",
#         "Ростелеком": "852361",
#         "Lesta Games": "856498",
#         "АТОЛ": "3343",
#         "Российское общество Знание": "3744247"
#     }
#     employers_id = [value for value in employers.values()]
#     vacancies = get_vac_list(employers_id)
#     for i in filter_fields(vacancies):
#         print(i)
#     input("pause")
#     total_vac = 0
#     for vacancy in vacancies:
#         total_vac += 1
#         print(vacancy)
#         print(vacancy["id"])
#         print(vacancy["alternate_url"])
#         print(vacancy["employer"]["name"])
#         print(vacancy["employer"]["id"])
#         print(vacancy["name"])
#         print(vacancy["area"]["name"])
#
#         if vacancy["salary"]:
#             print(
#                 f'Зарплата от {vacancy["salary"]["from"]} до {vacancy["salary"]["to"]} {vacancy["salary"]["currency"]}')
#         else:
#             print('Null')
#
#     print(f'Всего вакансий HH: {total_vac}')

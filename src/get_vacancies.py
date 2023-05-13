import json
import os
from datetime import datetime

import requests

from src.abstract_classes import GetVacancies


class HHVacancies(GetVacancies):
    """ Данный класс подключается к API hh.ru и получает вакансии.
    Полученные вакансии хранятся в классе в собственном формате.
    Все классы наследуемые от класса GetVacancies имеют одинаковый формат хранения вакансий."""

    __slots__ = ('url', 'params', 'search_fields', 'headers', 'response', 'vacancies', 'base',)

    def __init__(self):
        self.url: str = "https://api.hh.ru/vacancies"
        self.params: dict = {"text": "", "search_field": [], "per_page": 20, "period": 1}
        self.search_fields: list = ["name", "company_name", "description"]
        self.headers: str = ""
        self.response: int = 0
        self.vacancies: list = []
        self.base: str = "hh"

    def set_params(self, key: str, value: str | int) -> None:
        """ Метод получает в качестве параметров ключ и значение, которые добавляет в params запроса к API"""

        if key == "text":
            self.params["text"] = value
        # key search_field должен приходить в виде трёхсимвольной строки из цифр 1 или ноль - "101"
        # позиции единиц добавляют соответсвующее поле поиска из словаря self.search_fields:
        # ["name", "company_name", "description"]
        elif key == "search_field":
            self.params["search_field"] = []
            for i in range(3):
                if value[i] == "1":
                    self.params["search_field"].append(self.search_fields[i])
        elif key == "per_page":
            self.params["per_page"] = value
        elif key == "period":
            self.params["period"] = value
        else:
            print(f"Неверный параметр {key}")

    def reset_params(self) -> None:
        """ Метод сбрасывает значения params в состояние default"""

        self.params = {"text": "", "search_field": [], "per_page": 20, "period": 1}

    def set_headers(self) -> None:
        pass

    def get_vacancies(self) -> None:
        """ Метод запрашивает через API список вакансий, согласно фильтрам и сохраняет код response и данные"""

        response = requests.get(self.url, headers=self.headers, params=self.params)
        self.response = response.status_code
        if response.status_code == 200:
            self.vacancies = response.json()["items"]
        else:
            print(f"Ошибка запроса - {response.json()}")

    def display_vacancies(self) -> None:
        """Метод выводит на экран список полученных вакансий"""

        for item in self.vacancies:
            print(item)

    def provide_vacancies(self) -> list:
        """Метод проверяет наличие данных в ответе на запрос и, в случае успеха,
        преобразует вакансии к внутреннему формату и возвращает их в виде списка"""

        result = []
        self.get_vacancies()
        if self.response == 200 and self.vacancies:
            for vac in self.vacancies:

                if vac["salary"]:
                    salary_from = vac["salary"]["from"]
                    salary_to = vac["salary"]["to"]
                else:
                    salary_from = 0
                    salary_to = 0
                result.append({
                    "id_vac": "hh_" + vac["id"],
                    "name_vac": vac["name"],
                    "created_at": vac["created_at"][:10],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "place": vac["area"]["name"],
                    "url_vac": vac["alternate_url"],
                    "employer": vac["employer"]["name"],
                    "skills": vac["snippet"]["requirement"],
                    "charge": vac["snippet"]["responsibility"]
                })
        else:
            print("Нет вакансий по результатам запроса")
        return result

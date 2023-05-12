class Vacancies:
    """Данный класс инициализируется данными вакансий из класса, который унаследован от класса GetVacancies.
    Объекты класса хранятся в списке класса, который при помощи методов класса можно выводить на экран,
    сортировать по зарплате и выводить TOP N вакансий по зарплате с произвольным числом N."""

    __slots__ = ('id_vac', 'name_vac', 'created_at', 'salary_from', 'salary_to', 'place', 'url_vac', 'employer',
                 'skills', 'charge', 'salary',)
    all = []

    def __init__(self, data: dict):
        self.id_vac: str = data["id_vac"]
        self.name_vac: str = data["name_vac"]
        self.created_at: str = data["created_at"]
        self.salary_from: int = data["salary_from"]
        self.salary_to: int = data["salary_to"]
        self.place: str = data["place"]
        self.url_vac: str = data["url_vac"]
        self.employer: str = data["employer"]
        self.skills: str = data["skills"]
        self.charge: str = data["charge"]
        self.salary = self.__set_salary()
        self.all.append(self)

    def __set_salary(self):
        if not self.salary_from and not self.salary_to:
            return 0
        elif self.salary_from and self.salary_to:
            return max(self.salary_to, self.salary_from)
        elif not self.salary_from:
            return self.salary_to
        elif not self.salary_to:
            return self.salary_from

    def __lt__(self, other):
        """Метод сравнивает объекты по зарплате"""

        return self.salary < other.salary

    @classmethod
    def top_n(cls, n: int):
        """Метод возвращает TOP N вакансий по зарплате"""
        cls.all.sort(reverse=True)
        return cls.all[:n]

    def __str__(self):
        """Метод переопределяет строковое представление объекта класса"""

        give_str = f"Вакансия {self.id_vac}\n{self.created_at}\n{self.name_vac}\n{self.url_vac}\n"
        if not self.salary:
            give_str += "З\\П не указана\n"
        elif self.salary_from and self.salary_to:
            give_str += f"зарплата от {self.salary_from} до {self.salary_to}\n"
        elif self.salary_from:
            give_str += f"зарплата от {self.salary_from}\n"
        elif self.salary_to:
            give_str += f"зарплата до {self.salary_to}\n"
        give_str += f"{self.employer}\n{self.place}\n{self.skills}\n{self.charge}"
        return give_str

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id_vac}')"

    def display_vac(self):
        """Метод выводит список вакансий класса на экран"""

        for vac in self.all:
            print(vac)
        print(f"Всего вакансий - {len(Vacancies.all)}")

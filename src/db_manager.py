import os

import psycopg2


class DBManager:
    """Класс DBManager подключается к локальной БД Postgres по имении и получает информацию"""
    __slots__ = ('password', 'user', 'database', 'host',)

    def __init__(self, dbase_name: str):
        self.password: str = os.environ.get('PG_PASS')
        self.user: str ='postgres'
        self.database: str = dbase_name
        self.host: str = 'localhost'

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:

                with conn.cursor() as cur:
                    cur.execute("""SELECT employer_name, count(vacancy_id) FROM employers 
                                JOIN vacancies USING(employer_id) 
                                GROUP BY employer_name 
                                ORDER BY count(vacancy_id) DESC""")
                    result = cur.fetchall()

        finally:
            conn.close()
        return result

    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию."""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:

                with conn.cursor() as cur:
                    cur.execute("""SELECT employer_name, vacancy_name, salary, url FROM vacancies 
                                JOIN employers USING(employer_id) 
                                ORDER BY employer_name""")
                    result = cur.fetchall()

        finally:
            conn.close()
        return result

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:

                with conn.cursor() as cur:
                    cur.execute("""SELECT AVG(salary) FROM vacancies WHERE salary IS NOT null""")
                    result = int(cur.fetchone()[0])

        finally:
            conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:

                with conn.cursor() as cur:
                    cur.execute("""SELECT employer_name, vacancy_name, salary, url FROM vacancies 
                                JOIN employers USING(employer_id) 
                                WHERE salary IS NOT null AND 
                                salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT null) 
                                ORDER BY employer_name""")
                    result = cur.fetchall()

        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, key_word: str) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        key_word = "%"+key_word+"%"
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f"""SELECT employer_name, vacancy_name, salary, url FROM vacancies 
                                JOIN employers USING(employer_id) 
                                WHERE vacancy_name LIKE '{key_word}'
                                ORDER BY employer_name""")
                    result = cur.fetchall()
        finally:
            conn.close()
        return result


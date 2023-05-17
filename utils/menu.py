from src.db_manager import DBManager
from utils.insert_data import insert_data

hh_vac = DBManager('cw_5')


def main_menu() -> None:
    """Функция главного меню.
    Работает с локальной базой PostgreSQL 'cw_5'"""

    while True:
        option = input("Главное меню >\n" 
                       "[Парсинг вакансий]-1 [Статистика вакансий]-2 [Списки вакансий]-3 [Выход]-0 \n"
                       "(выбери число, нажми Enter)\n")
        if option == "1":
            menu_looking_vac()
        elif option == "2":
            statistics_vac()
        elif option == "3":
            lists_vac()
        elif option == "0":
            stop = input("Подтвердите завершение работы (Y) ")
            if stop.lower() == "y":
                exit()
        else:
            print("Неверный ввод, попробуйте ещё\n")


def menu_looking_vac() -> None:
    option = input("Главное меню > Парсинг вакансий >\n" 
                   "[Продолжить]-1 [Отменить]-0 \n"
                   "В базу будут загружены данные компаний из файла company_id.json (выбери число, нажми Enter)\n")
    if option == "1":
        insert_data()
    elif option == "0":
        print("Операция отменена")
    else:
        print("Неверный ввод, попробуйте ещё\n")


def statistics_vac() -> None:
    option = input("Главное меню > Статистика вакансий >\n"
                   "[Компании и кол-во вакансий]-1 [Средняя зарплата]-2 [Возврат]-0\n"
                   "(выбери число, нажми Enter)\n")
    if option == "1":
        for item in hh_vac.get_companies_and_vacancies_count():
            print(f"Компания {item[0]}, вакансий {item[1]}")
    elif option == "2":
        print("Средняя зарплата", hh_vac.get_avg_salary())
    elif option == "0":
        pass
    else:
        print("Неверный ввод, попробуйте ещё\n")


def lists_vac() -> None:
    option = input("Главное меню > Списки вакансий >\n"
                   "[Все вакансии]-1 [Вакансии с зарплатой выше средней]-2 [Фильтр вакансий по слову]-3 [Возврат]-0\n"
                   "(выбери число, нажми Enter)\n")
    if option == "1":
        for item in hh_vac.get_all_vacancies():
            print(item[0], item[1], item[2], item[3], sep=" <*> ")
    elif option == "2":
        for item in hh_vac.get_vacancies_with_higher_salary():
            print(item[0], item[1], item[2], item[3], sep=" <*> ")
    elif option == "3":
        key_word = input("Введите слово для поиска в названии вакансии\n")
        for item in hh_vac.get_vacancies_with_keyword(key_word):
            print(item[0], item[1], item[2], item[3], sep=" <*> ")
    elif option == "0":
        pass
    else:
        print("Неверный ввод, попробуйте ещё\n")

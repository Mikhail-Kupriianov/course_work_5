import os

import psycopg2 as psycopg2

from utils.get_employers import get_employers
from utils.get_vacancies import get_vac_list

PASS = os.environ.get('PG_PASS')


def insert_data() -> bool:
    result = False
    employers = get_employers()
    employers_id = [item[0] for item in employers]

    vacancies = get_vac_list(employers_id)

    conn = psycopg2.connect(host='localhost', database='cw_5', user='postgres', password=PASS)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO employers VALUES (%s, %s)", employers)
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)", vacancies)
        result = True

    finally:
        conn.close()
    return result

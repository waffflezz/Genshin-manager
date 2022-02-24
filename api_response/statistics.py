import os

import datetime
import sqlite3

from api_response.utils import gs
from pprint import pprint


dbpath = f'C:\\Users\\{os.environ.get("USERNAME")}\\PycharmProjects\\Genshin_manager\\databases\\'


def filtrate_dict(dictt, *keys):
    return {key: str(dictt[key]) for key in keys}


def make_primos_db(path):
    try:
        # создание базы данных + создание таблицы
        conn = sqlite3.connect(path + 'primogems.db')
        cursor = conn.cursor()

        # создание таблицы

        cursor.executescript(f"""
            BEGIN TRANSACTION;
            CREATE TABLE "primogem_base" (
                `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
                `time`    DATETIME ,
                `amount`    INTEGER,
                `reason`    TEXT,
                `uid`    TEXT
            );

            COMMIT;
            """)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print('Ошибка БД: ' + str(e))
        exit()


class StatisticsGetter:
    def __init__(self):
        self.path = os.getcwd()
        self.primos = gs.get_primogem_log(size=20, lang='ru-ru')
        self.resin = gs.get_resin_log(lang='ru-ru')

    def primos_db_upd(self):
        if 'primogems.db' not in os.listdir(dbpath):
            make_primos_db(dbpath)

        conn = sqlite3.connect(dbpath + 'primogems.db')
        cur = conn.cursor()

        for line_id, dct in enumerate(self.primos):
            line = filtrate_dict(dct, 'time', 'amount', 'reason', 'uid')
            cur.execute(f'''
            INSERT INTO 'primogem_base' (id, time, amount, reason, uid)
            VALUES({line_id}, {','.join([f"'{elem}'" for elem in line.values()])})
                        ''')
        conn.commit()
        conn.close()


stats = StatisticsGetter()
stats.primos_db_upd()
# while True:
#     trans = next(stats.primos)
#     if trans['time'].startswith(str(datetime.datetime.now())[:10]):
#
#     else:
#         break
# print(next(stats.primos))
# print()

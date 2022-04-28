import os

from pprint import pprint
import sqlite3 as sql


class DBaser:
    def __init__(self, storage: str):
        if not os.path.isdir(storage):
            os.makedirs(storage)
        self.db_storage = storage if storage.endswith('\\') else storage + '\\'
        self.db_types = {'stats': self.db_storage + 'statistics.db',
                         'wishes': self.db_storage + 'wishes.db'}

    def get_connection(self, db_type):
        conn = sql.connect(self.db_types[db_type])
        cur = conn.cursor()
        return conn, cur

    def make_statistics_base(self):
        conn, cur = self.get_connection('stats')
        cur.execute("""CREATE TABLE IF NOT EXISTS resin(
           trans_id INT PRIMARY KEY,
           reason TEXT,
           amount INTEGER,
           time TEXT,
           uid INTEGER
           );
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS primagems(
                   trans_id INT PRIMARY KEY,
                   reason TEXT,
                   amount INTEGER,
                   time TEXT,
                   uid INTEGER
                   );
                """)
        cur.execute("""CREATE TABLE IF NOT EXISTS dailys(
                           id INT PRIMARY KEY,
                           name TEXT,
                           amount INTEGER,
                           time TEXT,
                           img TEXT
                           );
                        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS artifacts(
                           id INT PRIMARY KEY,
                           name TEXT,
                           rarity INTEGER,
                           reason TEXT,
                           time TEXT,
                           uid INTEGER
                           );
                        """)
        conn.commit()

    def make_wishes_base(self):
        conn, cur = self.get_connection('wishes')
        table_names = ['novice_wishes', 'permanent_wish', 'character_event_wish', 'weapon_event_wish']
        for table in table_names:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table}(
                       id INT PRIMARY KEY,
                       name TEXT,
                       rarity INTEGER,
                       type TEXT, 
                       time TEXT,
                       uid INTEGER
                       );
                    """)
        conn.commit()

    @staticmethod
    def get_uids(cur):
        cur.execute("""SELECT uid from primagems""")
        uids = set(cur.fetchall()[0])
        cur.execute("""SELECT uid from artifacts""")
        uids.intersection(set(cur.fetchall()[0]))
        cur.execute("""SELECT uid from resin""")
        uids.intersection(set(cur.fetchall()[0]))
        return list(uids)

    @staticmethod
    def get_all(cur, db_type, select='*', where=None, reverse=True, order='trans_id'):
        req = f"""SELECT {select} FROM {db_type} """
        if where:
            req += f'WHERE {where} '
        req += f"ORDER BY {order}"
        if reverse:
            req += " DESC;"
        else:
            req += ";"
        cur.execute(req)

    @staticmethod
    def add_stat_line(stat, cur, values):
        cur.execute(f"""INSERT INTO {stat}(amount, trans_id, reason, time, uid) 
           VALUES({str(values).replace('[', '').replace(']', '')});""")

    @staticmethod
    def add_art_line(cur, values):
        cur.execute(f"""INSERT INTO artifacts(id, name, rarity, reason, time, uid) 
               VALUES({str(values).replace('[', '').replace(']', '')});""")

    @staticmethod
    def add_daily_line(cur, values):
        cur.execute(f"""INSERT INTO dailys(amount, time, img, name, id) 
                   VALUES({str(values).replace('[', '').replace(']', '')});""")

    @staticmethod
    def get_stat_page(stat, cur, start=None, amount=8):
        if start:
            cur.execute(f"""SELECT * FROM {stat} {'WHERE trans_id <= ' + start if start else ''}
                            ORDER BY trans_id DESC;""")
        else:
            cur.execute(f"""SELECT * FROM {stat}
                            ORDER BY trans_id DESC;""")
        return cur.fetchmany(amount)

    @staticmethod
    def stat_page(stat, cur, amount=8):
        start = None
        while True:
            cur.execute(f"""SELECT * FROM {stat} {'WHERE trans_id < ' + start if start else ''}
                                        ORDER BY trans_id DESC;""")
            res = cur.fetchmany(amount)
            if not res:
                raise StopIteration
            yield res
            start = str(res[-1][0])

    @staticmethod
    def art_page(cur, amount=8):
        start = None
        while True:
            cur.execute(f"""SELECT * FROM artifacts {'WHERE id < ' + start if start else ''}
                                                    ORDER BY id DESC;""")
            res = cur.fetchmany(amount)
            if not res:
                raise StopIteration
            yield res
            start = str(res[-1][0])

    @staticmethod
    def daily_page(cur, amount=8):
        start = None
        while True:
            cur.execute(f"""SELECT * FROM dailys {'WHERE id < ' + start if start else ''}
                                        ORDER BY id DESC;""")
            res = cur.fetchmany(amount)
            if not res:
                raise StopIteration
            yield res

            start = str(res[-1][0])


if __name__ == '__main__':
    baser = DBaser(f'C:\\Users\\{os.environ.get("USERNAME")}\\PycharmProjects\\Genshin_manager\\databases')
    baser.make_statistics_base()
    # baser.make_wishes_base()
    # conn, cur = baser.get_connection('stats')
    # aboba = baser.daily_page(cur)
    # pprint(next(aboba))
    # pprint(next(aboba))
    # pprint(next(aboba))

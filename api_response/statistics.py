import os

from datetime import datetime, date
from api_response.utils import gs
from pprint import pprint
from api_response.utils import test_workable, filtrate_dict, get_img_from_web, to_dict, str_to_datetime
from api_response.db_worker import DBaser
from sqlite3 import IntegrityError


class StatisticsGetter:
    def __init__(self, lang, db_storage=f'C:\\Users\\{os.environ.get("USERNAME")}'
                                        f'\\PycharmProjects\\Genshin_manager\\databases\\'):
        self.lang = lang

        self.db_path = db_storage
        self.baser = DBaser(self.db_path)
        self.conn, self.cur = self.baser.get_connection('stats')

        self.primos = self.baser.stat_page('primagems', self.cur)
        self.resin = self.baser.stat_page('resin', self.cur)
        self.dailys = self.baser.daily_page(self.cur)
        self.arts = self.baser.art_page(self.cur)

    @test_workable
    def get_next_page(self, stat_type, is_uid=False):
        td = {'resin': self.resin, 'primos': self.primos}
        return [to_dict(line[1:], 'reason', 'amount', 'time', 'uid') if is_uid else
                to_dict(line[1:], 'reason', 'amount', 'time')
                for line in next(td[stat_type])]

    @test_workable
    def get_arts_page(self, is_uid=False):
        return [to_dict(line[1:], 'name', 'rarity', 'reason', 'time', 'uid') if is_uid else
                to_dict(line[1:], 'name', 'rarity', 'reason', 'time')
                for line in next(self.arts)]

    @test_workable
    def get_dailys_page(self, is_pic=True):
        page = list(map(lambda x: to_dict(x[1:], 'name', 'count', 'date', 'img'), next(self.dailys)))
        if is_pic:
            for rew in page:
                rew['img'] = get_img_from_web(rew['img'])
        return page

    @test_workable
    def stat_db_update(self, reason):
        if reason == 'resin':
            stat = gs.get_resin_log(lang=self.lang)
        elif reason == 'primagems':
            stat = gs.get_primogem_log(lang=self.lang)
        else:
            raise 'Несуществующая причина обновления'

        counter = 0
        for field in stat:
            try:

                self.baser.add_stat_line(reason,
                                         self.cur,
                                         list(filtrate_dict(field, 'amount', 'id', 'reason', 'time', 'uid').values()))
            except IntegrityError:
                break
            counter += 1

        self.conn.commit()
        return f'{reason} db updated, added {counter} lines'

    @test_workable
    def arts_db_update(self):
        arts = gs.get_artifact_log(lang=self.lang)
        counter = 0

        for field in arts:
            try:
                self.baser.add_art_line(self.cur,
                                        list(filtrate_dict(field,
                                                           'id', 'name',
                                                           'rarity', 'reason',
                                                           'time', 'uid').values()))
            except IntegrityError:
                break
            counter += 1
            # break
        self.conn.commit()
        return f'artifacts db updated, added {counter} lines'

    @test_workable
    def daily_db_update(self):
        stat = gs.get_claimed_rewards()
        counter = 0
        for field in stat:

            try:
                self.baser.add_daily_line(self.cur,
                                          list(filtrate_dict(
                                              field,
                                              'cnt', 'created_at',
                                              'img', 'name', 'id').values()))
            except IntegrityError:
                break
            counter += 1
        self.conn.commit()
        return f'dailys db updated, added {counter} lines'

    def update_dbs(self):
        updates = [self.stat_db_update('primagems'),
                   self.stat_db_update('resin'),
                   self.arts_db_update(),
                   self.daily_db_update()]
        return updates

    def __del__(self):
        # self.conn.commit()
        self.conn.close()


class StatisticsAnalyzer:
    def __init__(self, db_storage=f'C:\\Users\\{os.environ.get("USERNAME")}'
                                  f'\\PycharmProjects\\Genshin_manager\\databases\\'):
        self.storage = db_storage
        self.baser = DBaser(self.storage)
        self.conn, self.cur = self.baser.get_connection('stats')

    def get_primos_per_month(self):
        self.cur.execute("""SELECT time from primagems ORDER BY trans_id DESC;""")
        months = {d: 0 for d in sorted(
            list(set(map(lambda x: tuple(map(int, x[0].split(' ')[0][:7].split('-'))), self.cur.fetchall()))))}
        self.cur.execute("""SELECT * from primagems
                            ORDER BY trans_id;""")
        while True:
            next_line = self.cur.fetchone()
            if next_line is None:
                break
            line = to_dict(next_line[1:], 'reason', 'amount', 'time', 'uid')
            line['time'] = str_to_datetime(line['time'])
            if (amount := line['amount']) > 0:
                months[(line['time'].year, line['time'].month)] += amount
        return months

    def get_primos_top(self):
        self.cur.execute("""SELECT reason, amount from primagems ORDER BY trans_id DESC;""")
        primo_top = {}
        while True:
            next_line = self.cur.fetchone()
            if next_line is None:
                break
            reason, amount = next_line
            if amount < 0:
                continue
            if reason not in primo_top.keys():
                primo_top[reason] = amount
            else:
                primo_top[reason] += amount
        return sorted(primo_top.items(), key=lambda x: int(x[1]), reverse=True)

    def get_primo_top_by_day(self):
        self.cur.execute("""SELECT time from primagems ORDER BY trans_id DESC;""")
        days = {d: [0] for d in sorted(
            list(set(map(lambda x: tuple(map(int, x[0].split(' ')[0].split('-'))), self.cur.fetchall()))))}
        self.cur.execute("""SELECT * from primagems
                                    ORDER BY trans_id;""")
        while True:
            next_line = self.cur.fetchone()
            if next_line is None:
                break
            line = to_dict(next_line[1:], 'reason', 'amount', 'time', 'uid')
            line['time'] = str_to_datetime(line['time'])
            if (amount := line['amount']) > 0:
                days[(line['time'].year, line['time'].month, line['time'].day)][0] += amount
        return list(map(lambda x: {x[0]: x[1]}, sorted(days.items(), key=lambda x: x[1], reverse=True)))

    def __del__(self):
        self.conn.close()


class WishesGetter:
    def __init__(self, lang, db_storage=f'C:\\Users\\{os.environ.get("USERNAME")}'
                                        f'\\PycharmProjects\\Genshin_manager\\databases\\'):
        self.lang = lang

        self.db_path = db_storage
        self.baser = DBaser(self.db_path)
        self.conn, self.cur = self.baser.get_connection('wishes')

    def wishes_db_update(self):
        wishes = gs.get_wish_history()
        return [next(wishes) for i in range(5)]


if __name__ == '__main__':
    from utils import set_cookie

    set_cookie('cookie.txt')
    stats = StatisticsGetter('ru-ru')
    # print(stats.update_dbs())
    analyzer = StatisticsAnalyzer()

    pprint(analyzer.get_primos_per_month())
    # pprint(analyzer.get_primo_top_by_day())

import os

from api_response.utils import gs
from pprint import pprint
from api_response.utils import (test_workable,
                                timer,
                                filtrate_dict,
                                get_img_from_web,
                                to_dict,
                                str_to_datetime,
                                sec_from_time)
from api_response.db_worker import DBaser
from sqlite3 import IntegrityError


class StatisticsGetter:

    def __init__(self, lang, db_storage='C:\\ProgramData\\Genshin_manager\\databases\\', is_auto_update=False):
        self.lang = lang

        self.db_path = db_storage
        self.baser = DBaser(self.db_path)
        self.conn, self.cur = self.baser.get_connection('stats')
        self.primos = self.baser.stat_page('primagems', self.cur)
        self.resin = self.baser.stat_page('resin', self.cur)
        self.dailys = self.baser.daily_page(self.cur)
        self.arts = self.baser.art_page(self.cur)
        if is_auto_update:
            self.update_dbs()

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

    @timer
    @test_workable
    def stat_db_update(self, reason):
        last_id = 0
        counter = 0
        while True:
            if reason == 'resin':
                stat = gs.get_resin_log(lang=self.lang, size=20, end_id=last_id)
            elif reason == 'primagems':
                stat = gs.get_primogem_log(lang=self.lang, size=20, end_id=last_id)
            else:
                raise 'Несуществующая причина обновления'
            ids = self.baser.get_ids(self.cur, reason, 'trans_id')
            vals = list(
                filter(
                    lambda x: x[1] not in list(
                        map(
                            lambda y: str(y[0]), ids
                        )
                    ),
                    map(
                        lambda field: list(
                            filtrate_dict(field, 'amount', 'id', 'reason', 'time', 'uid').values()
                        ), stat
                    )
                )
            )

            if vals:
                last_id = vals[-1][1]
                self.baser.add_stat_line(reason,
                                         self.cur,
                                         vals)
                counter += len(vals)
            else:
                break

        self.conn.commit()
        return f'{reason} db updated, added {counter} lines'

    @timer
    # @test_workable
    def arts_db_update(self):
        last_id = 0
        counter = 0
        while True:
            arts = gs.get_artifact_log(lang=self.lang, size=20, end_id=last_id)
            vals = list(filter(lambda x: x[0] not in list(map(lambda y: str(y[0]),
                                                              self.baser.get_ids(self.cur, 'artifacts', 'id'))),
                               map(lambda field:
                                   list(filtrate_dict(field,
                                                      'id', 'name',
                                                      'rarity', 'reason',
                                                      'time', 'uid').values()), arts)))
            if vals:
                last_id = vals[-1][0]
                self.baser.add_art_line(self.cur, vals)
                counter += len(vals)
            else:
                break
            counter += 1
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

    @timer
    @test_workable
    def update_dbs(self):
        updates = [self.stat_db_update('primagems'),
                   self.stat_db_update('resin'),
                   self.arts_db_update(),
                   self.daily_db_update()]
        self.update_generators()
        return updates

    def update_generators(self):
        self.primos = self.baser.stat_page('primagems', self.cur)
        self.resin = self.baser.stat_page('resin', self.cur)
        self.dailys = self.baser.daily_page(self.cur)
        self.arts = self.baser.art_page(self.cur)

    def __del__(self):
        # self.conn.commit()
        self.conn.close()


class StatisticsAnalyzer:
    def __init__(self, db_storage='C:\\ProgramData\\Genshin_manager\\databases\\'):
        self.storage = db_storage
        self.baser = DBaser(self.storage)
        self.conn, self.cur = self.baser.get_connection('stats')
        self.cur.execute("""SELECT uid from primagems""")
        self.uids = self.baser.get_uids(self.cur)

    @test_workable
    def get_primos_per_month(self, uid=None):
        if uid is None:
            uid = self.uids[0]

        self.baser.get_all(self.cur, 'primagems', where=f'uid={uid}', select='time')
        months = {d: 0 for d in sorted(
            list(set(map(lambda x: tuple(map(int, x[0].split(' ')[0][:7].split('-'))), self.cur.fetchall()))))}
        self.baser.get_all(self.cur, 'primagems', where=f'uid={uid}')

        while True:
            next_line = self.cur.fetchone()
            if next_line is None:
                break
            line = to_dict(next_line[1:], 'reason', 'amount', 'time', 'uid')
            line['time'] = str_to_datetime(line['time'])
            if (amount := line['amount']) > 0:
                months[(line['time'].year, line['time'].month)] += amount
        return months

    @test_workable
    def get_primos_top(self, uid=None):
        if uid is None:
            uid = self.uids[0]
        self.baser.get_all(self.cur, 'primagems', select='reason, amount', where=f'uid={uid}')
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
        return list(map(lambda x: {'reason': x[0], 'amount': x[1]},
                        sorted(primo_top.items(), key=lambda x: int(x[1]), reverse=True)))

    @test_workable
    def get_primo_top_by_day(self, uid=None):
        if uid is None:
            uid = self.uids[0]
        self.baser.get_all(self.cur, 'primagems', select='time', where=f'uid={uid}')
        days = sorted(
            list(set(map(lambda x: x[0].split(' ')[0], self.cur.fetchall()))), reverse=True)

        fat_days = []
        for day in days:
            self.baser.get_all(self.cur, 'primagems',
                               select='reason, amount, time, uid',
                               where=f"time LIKE '{day}%' AND uid={uid}")

            day_acts = list(filter(lambda x: x[1] > 0, map(lambda x: list(x[:-1]), self.cur.fetchall())))

            primo_sum = 0
            for x, d in enumerate(day_acts):
                d[2] = d[2].split(' ')[1]
                day_acts[x] = to_dict(d, 'reason', 'amount', 'time')
                primo_sum += day_acts[x]['amount']
            fat_days.append({'day': day,
                             'amount': primo_sum,
                             'acts': sorted(day_acts, key=lambda x: sec_from_time(x['time']))})

        fat_days = sorted(fat_days, key=lambda x: x['amount'], reverse=True)

        x60len = len([x for x in fat_days if x['amount'] <= 60])
        first_60_index = [i['amount'] for i in fat_days].index(60) + 1
        del fat_days[first_60_index:]
        for trans in fat_days[-1]['acts']:
            del trans['time']
        del fat_days[-1]['day']
        fat_days[-1]['days_count'] = x60len
        # print(x60len, first_60_index)
        # return 0
        return fat_days

    def __del__(self):
        self.conn.close()


class WishesGetter:
    def __init__(self, lang, db_storage='C:\\ProgramData\\Genshin_manager\\databases\\'):
        self.lang = lang

        self.db_path = db_storage
        self.baser = DBaser(self.db_path)
        self.conn, self.cur = self.baser.get_connection('wishes')

    def wishes_db_update(self):
        wishes = gs.get_wish_history()
        return [next(wishes) for i in range(5)]


if __name__ == '__main__':
    from utils import set_cookie

    set_cookie()
    stats = StatisticsGetter('ru-ru', is_auto_update=False)
    pprint(stats.stat_db_update('primagems'))

    # print(stats.get_next_page('resin'))
    # print(stats.update_dbs())
    analyzer = StatisticsAnalyzer()

    # print('get_primos_per_month')
    # pprint(analyzer.get_primos_per_month())
    # print('\nget_primos_top')
    # pprint(analyzer.get_primos_top())
    print('\nget_primo_top_by_day')
    pprint(analyzer.get_primo_top_by_day()[-5:])

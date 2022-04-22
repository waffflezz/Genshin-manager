import os

from api_response.utils import gs
from pprint import pprint
from api_response.utils import test_workable, filtrate_dict, get_img_from_web, to_dict
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

    @test_workable
    def get_next_page(self, stat_type, is_uid=False):
        td = {'resin': self.resin, 'primos': self.primos}
        return [to_dict(line[1:], 'reason', 'amount', 'time', 'uid') if is_uid else
                to_dict(line[1:], 'reason', 'amount', 'time')
                for line in next(td[stat_type])]

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
        self.stat_db_update('primagems')
        self.stat_db_update('resin')
        self.daily_db_update()


if __name__ == '__main__':
    from utils import set_cookie

    set_cookie('cookie.txt')
    stats = StatisticsGetter('ru-ru')
    pprint(stats.get_dailys_page())
    # pprint(stats.get_next_page('resin'))

    stats.conn.close()

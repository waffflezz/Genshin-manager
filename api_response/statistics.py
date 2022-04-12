import os

import genshinstats.errors

from api_response.utils import gs
from pprint import pprint
from utils import test_workable, filtrate_dict, get_img_from_web

dbpath = f'C:\\Users\\{os.environ.get("USERNAME")}\\PycharmProjects\\Genshin_manager\\databases\\'


class StatisticsGetter:
    def __init__(self, lang):
        self.primos = gs.get_primogem_log(lang=lang)
        self.resin = gs.get_resin_log(lang=lang)
        self.dailys = gs.get_claimed_rewards()

    @test_workable
    def get_next_page(self, stat_type, amount=8, is_uid=False):
        td = {'resin': self.resin, 'primos': self.primos}
        page = []
        for i in range(amount):
            try:
                if is_uid:
                    page.append(filtrate_dict(next(td[stat_type]), 'amount', 'reason', 'time', 'uid'))
                else:
                    page.append(filtrate_dict(next(td[stat_type]), 'amount', 'reason', 'time'))
            except StopIteration:
                break
        return page

    @test_workable
    def get_dailys_page(self, amount=8):
        page = []
        for _ in range(amount):
            try:
                elem = filtrate_dict(next(self.dailys), 'cnt', 'created_at', 'name', 'img')
            except StopIteration:
                break
            elem['img'] = get_img_from_web(elem['img'])
            elem['created_at'] = elem['created_at'].split(' ')[0]
            page.append({'name': elem['name'], 'count': elem['cnt'], 'date': elem['created_at'], 'img': elem['img']})
        return page


if __name__ == '__main__':
    from utils import set_cookie

    set_cookie('cookie.txt')
    stats = StatisticsGetter('ru-ru')
    pprint(stats.get_dailys_page(amount=8))
    # pprint(stats.get_next_page('primos', amount=10, is_uid=True))

# while True:
#     trans = next(stats.primos)
#     if trans['time'].startswith(str(datetime.datetime.now())[:10]):
#
#     else:
#         break
# print(next(stats.primos))
# print()

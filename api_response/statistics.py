import os


from api_response.utils import gs
from pprint import pprint

dbpath = f'C:\\Users\\{os.environ.get("USERNAME")}\\PycharmProjects\\Genshin_manager\\databases\\'


def filtrate_dict(dictt, *keys):
    return {key: str(dictt[key]) for key in keys}


class StatisticsGetter:
    def __init__(self, lang):
        self.primos = gs.get_primogem_log(lang=lang)
        self.resin = gs.get_resin_log(lang=lang)

    def get_next_page(self, type, amount=8, is_uid=False):
        td = {'resin': self.resin, 'primos': self.primos}
        page = []
        for i in range(amount):
            if is_uid:
                page.append(filtrate_dict(next(td[type]), 'amount', 'reason', 'time', 'uid'))
            else:
                page.append(filtrate_dict(next(td[type]), 'amount', 'reason', 'time'))
        return page


if __name__ == '__main__':
    stats = StatisticsGetter('ru-ru')
    pprint(stats.get_next_page('resin', amount=10, is_uid=True))

# while True:
#     trans = next(stats.primos)
#     if trans['time'].startswith(str(datetime.datetime.now())[:10]):
#
#     else:
#         break
# print(next(stats.primos))
# print()

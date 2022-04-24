import os
import traceback

from datetime import datetime
from pprint import pprint
import genshinstats as gs

from urllib.request import urlopen

cookie_path = os.path.dirname(os.path.abspath(__file__)) + r'\cookie.txt'


def set_cookie(path):
    with open(path) as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


def get_active_uids():
    accs = sorted(list(map(lambda y: filtrate_dict(y, 'level', 'nickname', 'server', 'uid'),
                           filter(lambda x: x['nickname'] != '玩家' + str(x['uid']), gs.get_game_accounts()))),
                  key=lambda x: int(x['level']), reverse=True)
    return accs


def is_cookie():
    set_cookie(cookie_path)
    try:
        gs.claim_daily_reward()
    except gs.errors.NotLoggedIn:
        return False
    return True


def get_img_from_web(img):
    resource = urlopen(img)
    return resource.read()


def get_time_from_sec(seconds, lang):
    hours, ost = divmod(int(seconds), 3600)
    sec, mins = divmod(ost, 60)
    if lang == 'ru-ru':
        return f'{hours}ч:{mins}м:{sec}с'
    elif lang == 'en-us':
        return f'{hours}h:{mins}m:{sec}s'


def filtrate_dict(dictt, *keys):
    return {key: str(dictt[key]) for key in keys}


def to_dict(arr, *keys):
    res = {}
    for key, val in zip(keys, arr):
        res[key] = val
    return res


def test_workable(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            stack = traceback.extract_stack()
            return f'{stack} -> {e}'
        return res

    return wrapper


def str_to_datetime(string:str):
    date, time = string.split(' ')
    date = list(map(int, date.split('-')))
    time = list(map(int, time.split(':')))
    return datetime(*date, *time)


if __name__ == '__main__':
    set_cookie('cookie.txt')
    # pprint(get_active_uids())
    # next(gs.get_primogem_log())

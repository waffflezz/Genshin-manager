import os
import functools

from datetime import datetime
from time import time

from pprint import pprint
import genshinstats as gs

from urllib.request import urlopen


def set_cookie(path='C:\\ProgramData\\Genshin_manager\\cookie.txt'):
    with open(path) as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = time()
        res = func(*args, **kwargs)
        te = time()
        print(f'"{func.__name__}" completed for {te - ts:.4f} secs')
        return res

    return wrapper


def get_active_uids():
    accs = sorted(list(map(lambda y: filtrate_dict(y, 'level', 'nickname', 'server', 'uid'),
                           filter(lambda x: x['nickname'] != '玩家' + str(x['uid']), gs.get_game_accounts()))),
                  key=lambda x: int(x['level']), reverse=True)
    for acc in accs:
        acc['level'] = int(acc['level'])
    return accs


def is_cookie():
    set_cookie()
    try:
        gs.claim_daily_reward()
    except gs.errors.NotLoggedIn:
        return False
    return True


def is_authkey():
    try:
        next(gs.get_primogem_log())
    except gs.AuthkeyError or gs.AuthkeyTimeout or gs.InvalidAuthkey or gs.MissingAuthKey:
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


def sec_from_time(ttime):
    h, m, s = list(map(int, ttime.split(':')))

    return (h * 24 + m) * 60 + s


def filtrate_dict(dictt, *keys):
    return {key: str(dictt[key]) for key in keys}


def to_dict(arr, *keys):
    res = {}
    for key, val in zip(keys, arr):
        res[key] = val
    return res


def test_workable(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            print(f'{func.__name__} -> {e}')
            return e
        return res

    return wrapper


def str_to_datetime(string: str):
    date, time = string.split(' ')
    date = list(map(int, date.split('-')))
    time = list(map(int, time.split(':')))
    return datetime(*date, *time)


@test_workable
def test(it):
    return next(it)


def translate_dict_keys(dct, translator, lang):
    keys = list(dct.keys())
    for key in keys:
        val = translator.get(key, False)
        if val:
            dct[val[lang]] = dct[key]
            del dct[key]
    return dct


if __name__ == '__main__':
    from api_response.abyss import Abyss

    set_cookie()
    uid = 705359736
    rus = 'ru-ru'
    eng = 'en-us'
    set_cookie()
    ab = Abyss(uid, rus)
    pprint(translate_dict_keys(ab.get_abyss_stats(ab.pre_abyss)['stats'], ab.translate, rus))

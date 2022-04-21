import os
import genshinstats as gs

from urllib.request import urlopen

cookie_path = os.path.dirname(os.path.abspath(__file__)) + r'\cookie.txt'


def set_cookie(path):
    with open(path) as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


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
            return e
        return res

    return wrapper


if __name__ == '__main__':
    # set_cookie('cookie.txt')
    print(to_dict(('Расходные материалы для алхимии',
             '-40',
             '2022-04-19 17:49:27',
             '705359736'), 'name', 'amount', 'time', 'uid'))

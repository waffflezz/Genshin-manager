import genshinstats as gs

from urllib.request import urlopen
from requests.exceptions import HTTPError


def set_cookie(path):
    with open(path) as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


def is_cookie():
    try:
        gs.fetch_endpoint('')
    except gs.errors.NotLoggedIn:
        return False
    except HTTPError:
        return True
    return 'Произошла неведомая хрень'


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


def test_workable(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            return e
        return res

    return wrapper


import genshinstats as gs
import requests
from urllib.request import urlopen
from pprint import pprint


def set_cookie():
    with open('cookie.txt') as cook:
        ltoken = cook.readline().replace('\n', '')
        ltuid = cook.readline().replace('\n', '')
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)


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


def grab_notes(uid, lang):
    trans = {'completed_commissions': {'ru-ru': 'Сделано дейликов: ',
                                       'en-us': 'Completed commissions: '},
             'claimed_commission_reward': {'ru-ru': 'Награда за дейлики у Катерины: ',
                                           'en-us': 'Katherin reward: '},
             'claimed': {'ru-ru': 'собрана',
                         'en-us': 'claimed'},
             'not_claimed': {'ru-ru': 'не собрана',
                             'en-us': 'not claimed'},
             'remaining_boss_discounts': {'ru-ru': 'Осталось зафармить боссв: ',
                                          'en-us': 'Farmed bosses: '},
             'resin': {'ru-ru': 'Смолы: ',
                       'en-us': 'Resin: '},
             'until_resin_limit': {'ru-ru': 'До полного восстановления: ',
                                   'en-us': 'Until the complite restoration: '},
             'expeditions': {'ru-ru': 'Экспедиции: ',
                             'en-us': 'Expeditions: '},
             'remaining_time': {'ru-ru': '    Осталось: ',
                                'en-us': '    Time left: '}
             }

    response = gs.get_notes(uid, lang=lang)

    res_text = []

    res_text.append(
        f"{trans['completed_commissions'][lang]}{response['completed_commissions']}\\{response['total_commissions']}")

    is_claimed = trans['claimed'][lang] if response['claimed_commission_reward'] is True else trans['not_claimed'][lang]
    res_text.append(f"{trans['claimed_commission_reward'][lang]}{is_claimed}")

    res_text.append(f"{trans['remaining_boss_discounts'][lang]}"
                    f"{response['remaining_boss_discounts']}"
                    f"\\{response['max_boss_discounts']}")

    res_text.append(f"{trans['resin'][lang]}"
                    f"{response['resin']}\\{response['max_resin']}\n"
                    f"{trans['until_resin_limit'][lang]}"
                    f"{get_time_from_sec(response['until_resin_limit'], lang)}")

    res_text.append(f"{trans['expeditions'][lang]}"
                    f"{len(list(filter(lambda expa: expa['remaining_time'] != 0, response['expeditions'])))}"
                    f"\\{response['max_expeditions']}")

    for exp in response['expeditions']:
        res_text.append((get_img_from_web(exp['icon']),
                         f"{trans['remaining_time'][lang]}"
                         f"{get_time_from_sec(exp['remaining_time'], lang)}"))

    return res_text


if __name__ == '__main__':
    set_cookie()
    uid = 705359736
    rus = 'ru-ru'
    eng = 'en-us'
    pprint(grab_notes(uid, eng))

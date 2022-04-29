from api_response.utils import gs
from api_response.utils import get_img_from_web, get_time_from_sec, test_workable


@test_workable
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

    res_text = {'info': {}, 'characters': []}

    info = res_text['info']
    info['dailik'] = f"{trans['completed_commissions'][lang]}" \
                     f"{response['completed_commissions']}\\" \
                     f"{response['total_commissions']}"

    is_claimed = trans['claimed'][lang] if response['claimed_commission_reward'] is True else trans['not_claimed'][lang]
    info['reward'] = f"{trans['claimed_commission_reward'][lang]}{is_claimed}"
    info['bosses'] = f"{trans['remaining_boss_discounts'][lang]}" \
                     f"{response['remaining_boss_discounts']}\\{response['max_boss_discounts']}"

    info['resin'] = f"{trans['resin'][lang]}" \
                    f"{response['resin']}\\{response['max_resin']}\n" \
                    f"{trans['until_resin_limit'][lang]}" \
                    f"{get_time_from_sec(response['until_resin_limit'], lang)}"

    info['expedition'] = f"{trans['expeditions'][lang]}" \
                         f"{len(list(filter(lambda expa: expa['remaining_time'] != 0, response['expeditions'])))}" \
                         f"\\{response['max_expeditions']}"

    for exp in response['expeditions']:
        res_text['characters'].append({'img': get_img_from_web(exp['icon']),
                                       'time': f"{trans['remaining_time'][lang]}"
                                               f"{get_time_from_sec(exp['remaining_time'], lang)}"})

    return res_text


if __name__ == '__main__':
    from utils import set_cookie
    from pprint import pprint

    set_cookie()
    uid = 705359736
    rus = 'ru-ru'
    eng = 'en-us'
    pprint(grab_notes(uid, rus))

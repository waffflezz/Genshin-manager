from api_response.utils import gs, get_active_uids, translate_dict_keys
from utils import set_cookie
from pprint import pprint


def grab_abyss(uid, lang):
    res_abyss = []
    for floor in gs.get_spiral_abyss(uid=uid, previous=True)['floors']:
        res_floor = {'Этаж': floor['floor'],
                     'Звезд': floor['stars']}
        print(floor['floor'])
        res_floor['Залы'] = []
        for chamber in floor['chambers']:
            res_floor['Залы'].append(chamber["chamber"])
            print('\t', f'Зал - {chamber["chamber"]} Звезд: {chamber["stars"]}')
            print('\t\t', chamber['battles'])

    return []


class Abyss:
    def __init__(self, uid=None, lang='ru-ru'):
        self.uid = get_active_uids()[0]['uid'] if uid is None else uid
        self.lang = lang
        self.now_abyss = gs.get_spiral_abyss(uid=self.uid)
        self.pre_abyss = gs.get_spiral_abyss(uid=self.uid, previous=True)
        self.translate = {'most_bursts_used': {'ru-ru': "Выполнено взрывов стихий:",
                                               'en-us': "Elemental bursts unleashed"},
                          'most_damage_taken': {'ru-ru': "Макс. полученного урона:",
                                                'en-us': "Most damage taken:"},
                          'most_kills': {'ru-ru': "Максимум убийств:",
                                         'en-us': "Most kills:"},
                          'most_played': {'ru-ru': "Наиболее популярные персонажи:",
                                          'en-us': "Most played characters:"},
                          'most_skills_used': {'ru-ru': "Выполнено элементальных навыкв:",
                                               'en-us': "Elemental skills cast:"},
                          'strongest_strike': {'ru-ru': "Самый мощный удар:",
                                               'en-us': "Strongest single strike:"},
                          'max_floor': {'ru-ru': "Макс. этаж:",
                                        'en-us': "Deepest descent:"},
                          'total_battles': {'ru-ru': "Всего битв:",
                                            'en-us': "Battles fought:"},
                          'total_stars': {'ru-ru': "Звезд:",
                                          'en-us': "Stars:"},
                          'total_wins': {'ru-ru': "Побед:",
                                         'en-us': "Wins:"},
                          }

    @staticmethod
    def get_floors(abyss):
        return [floor['floor'] for floor in abyss['floors']]

    def get_floor(self, abyss, floor_n):

        if floor_n not in self.get_floors(abyss):
            raise "Floor not passed"
        tfloor = next(filter(lambda x: x['floor'] == floor_n, abyss['floors']))
        tfloor['stars'] = f'{tfloor["stars"]}/{tfloor["max_stars"]}'

        del tfloor['max_stars'], tfloor['floor'], tfloor['icon'], tfloor['start']

        return tfloor['chambers'][0]

    def get_abyss_stats(self, abyss):
        res = {'character_ranks': translate_dict_keys(abyss['character_ranks'], self.translate, self.lang),
               'stats': translate_dict_keys(abyss['stats'], self.translate, self.lang)}
        return res


if __name__ == '__main__':
    uid = 705359736
    rus = 'ru-ru'
    eng = 'en-us'
    set_cookie()
    ab = Abyss(uid, rus)
    pprint(ab.get_floor(ab.pre_abyss, 9))
    # pprint(ab.get_abyss_stats(ab.pre_abyss))

    # print(*grab_abyss(uid, rus), sep='\n')

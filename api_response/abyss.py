from api_response.utils import gs


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


if __name__ == '__main__':
    from utils import set_cookie
    from pprint import pprint

    uid = 705359736
    rus = 'ru-ru'
    eng = 'en-us'
    print(*grab_abyss(uid, rus), sep='\n')

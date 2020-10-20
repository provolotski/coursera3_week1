import requests
import time
import datetime


def calc_age(uid):
    friend_dict = {}
    for item in get_user_friend_list(get_user_id(uid)):
        if is_valid_date(item.get('bdate')):
            if friend_dict.get(get_age(item.get('bdate')))is None:
                friend_dict[get_age(item.get('bdate'))] =1
            else:
                friend_dict[get_age(item.get('bdate'))] += 1
    friend_list = [(k, v) for k,v in friend_dict.items()]

    return sorted(friend_list, key=lambda friend: (-friend[1], friend[0]))


def get_age(date):
    return datetime.date.today().year - time.strptime(date, '%d.%m.%Y').tm_year

def is_valid_date(date):
    if date is None:
        return False
    else:
        try:
            time.strptime(date, '%d.%m.%Y')
            return True
        except ValueError:
            return False


def get_user_id(uid):
    params = getconstantparams()
    params['user_ids'] = uid
    response = requests.get(URL_user_gets, params=params)
    return response.json().get('response')[0].get('id')


def get_user_friend_list(uid):
    params = getconstantparams()
    params['user_id'] = uid
    params['fields'] = 'bdate'
    response = requests.get(URL_friends_get, params=params)
    return response.json().get('response').get('items')


def getconstantparams():
    return {'v': API_Version, 'access_token': ACCESS_TOKEN}


# sample url = ''
# Constant block
URL_user_gets = 'https://api.vk.com/method/users.get'
URL_friends_get = 'https://api.vk.com/method/friends.get'
ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
API_Version = '5.71'

if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

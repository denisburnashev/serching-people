import requests
import vk_api
import random
from datetime import date
from pprint import pprint

with open('VKtoken.txt', 'r') as file_object:
    vktoken = file_object.read().strip()

with open('group_token.txt', 'r') as file_object:
    token = file_object.read().strip()


people_list = []

today = str(date.today())
today_year = today[0:4]


class Bot:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    # def user_get(self, user_id=None):
    #
    #     if user_id is None:
    #         user_id = self.owner_id
    #     user_get_url = self.url + 'users.get'
    #     user_get_params = {
    #         'users_ids': user_id,
    #         'fields': 'bdate, sex, city, relation'
    #     }
    #     res = requests.get(user_get_url, params={**self.params, **user_get_params})
    #     res = res.json()
    #     data = res['response']
    #     for info in data:
    #         print(info['city'])
    #         user_age.append(info['bdate'][5:])
    #         user_sex.append(info['sex'])
    #         user_city.append(info['city']['id'])
    #         user_relation.append(info['relation'])

    def users_search(self, user_id):

        user_search_url = self.url + 'users.get'
        user_search_params = {
            'users_ids': user_id,
            'fields': 'bdate, sex, city'
        }
        res = requests.get(user_search_url, params={**self.params, **user_search_params})
        res = res.json()
        data = res['response']
        pprint(data)
        for info in data:
            if info['sex'] == 2:
                user_sex = 1
            elif info['sex'] == 1:
                user_sex = 2
            city_id = info['city']['id']
            age_from = int(today_year) - int(info['bdate'][5:]) - 2
            age_to = int(today_year) - int(info['bdate'][5:]) + 2

        search_url = self.url + 'users.search'
        offset = 0
        users_search_params = {
            'count': 10,
            'city': city_id,
            'sex': user_sex,
            'status': 6,
            'age_from': age_from,
            'age_to': age_to
        }
        res = requests.get(search_url, params={**self.params, **users_search_params})
        res = res.json()
        data = res['response']['items']
        # while offset <= count:
        #     users_search_params = {
        #     'offset': offset,
        #     'count': 10,
        #     'city': city_id,
        #     'sex': user_sex,
        #     'status': 6,
        #     'age_from': age_from,
        #     'age_to': age_to
        #     }
        #     res = requests.get(search_url, params={**self.params, **users_search_params})
        #     res = res.json()
        #     data = res['response']['items']
        url = 'https://vk.com/id'
        for item in data:
            people_list.append(url + str(item['id']))
            # offset = offset + users_search_params['count']

    def user_search_your_settings(self, sex, age_from, age_to, city):

        search_url = self.url + 'users.search'
        offset = 0
        users_search_params = {
            'offset': 0,
            'count': 10,
            'city': city,
            'sex': sex,
            'status': 6,
            'age_from': age_from,
            'age_to': age_to
        }
        res = requests.get(search_url, params={**self.params, **users_search_params})
        res = res.json()
        count = res['response']['count']
        pprint(count)
        while offset <= count:
            users_search_params = {
                'offset': offset,
                'count': 10,
                'city': city,
                'sex': sex,
                'status': 6,
                'age_from': age_from,
                'age_to': age_to
            }
            res = requests.get(search_url, params={**self.params, **users_search_params})
            res = res.json()
            data = res['response']['items']
            url = 'https://vk.com/id'
            for item in data:
                print(url + str(item['id']))
            offset = offset + users_search_params['count']


vkbot = Bot(vktoken, '5.126')
vk = vk_api.VkApi(token=token)
vk._auth_token()


def main():
    while True:
        messages = vk.method('messages.getConversations', {'filter': 'unanswered'})
        if messages['count'] >= 1:
            text = messages['items'][0]['last_message']['text']
            user_id = messages['items'][0]['last_message']['from_id']
            if text == 'Ку' or text == 'ку' or text == 'Хай' or text == 'хай' or text == 'Привет' or text == 'привет':
                vk.method('messages.send', {
                    'user_id': user_id,
                    'message': 'Привет это бот - vkinder по поиску людей.\n'
                               'Для кого ты хочешь найти подходящих людей?\n'
                               'Если ты хочешь найти для себя просто напиши - себе,\n'
                               'а если ты хочешь найти для друга введи - другу',
                    'random_id': random.randint(1, 1000)})
            elif text == 'Себе' or text == 'себе':
                vk.method('messages.send', {
                    'user_id': user_id,
                    'message': 'Отлично, ты хочешь найти человека для себя\n'
                               'Я могу предложить два варианта поиска:\n'
                               'если интересует быстрый поиск просто введи быстрый поиск\n'
                               'если же интересует детальный поиск просто введи детальный поиск',
                    'random_id': random.randint(1, 1000)})
            elif text == 'быстрый поиск':
                vkbot.users_search(user_id)
                for people_url in people_list:
                    vk.method('messages.send', {
                        'user_id': user_id,
                        'message': people_url,
                        'random_id': random.randint(1, 1000)
                    })
            elif text == 'Другу' or text == 'другу':
                vk.method('messages.send', {
                    'user_id': user_id,
                    'message': 'Отлично, ты хочешь найдти для друга ',
                    'random_id': random.randint(1, 1000)})
            else:
                vk.method('messages.send', {
                    'user_id': user_id,
                    'message': 'Не понятно',
                    'random_id': random.randint(1, 1000)
                })


main()
# 14869974

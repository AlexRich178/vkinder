import threading
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from auth_data import group_token
from auth_data import personal_token
from keyboards import *
from server import server_start
from db import session, BotUsers, Favorites, OpenSearchData, SearchingParams
from sqlalchemy import exists, func
import json

GROUP_ID = 213215624
GROUP_TOKEN = group_token
PERSONAL_TOKEN = personal_token
API_VERSION = '5.131'

# типы колбэк кнопок
CALLBACK_TYPES = ('show_snackbar', 'open_link')

# возраст
AGES = {
    'age1': [18, 25],
    'age2': [25, 35],
    'age3': [35, 45],
    'age4': [45, 55],
    'age5': [55, 65],
    'age6': [65, 75],
    'age7': [75, 85],
    'age8': [85, 95]
}

# пол
SEX = {
    'male': 2,
    'female': 1,

}


# определение города юзера
def user_city(user_id):
    data = pvk.users.get(
        user_ids=user_id,
        fields='city')
    return data[0]['city']['id']


# полное имя
def user_name(user_id):
    data = pvk.users.get(
        user_ids=user_id,
        name_case='nom')
    full_name = data[0]['first_name'] + ' ' + data[0]['last_name']
    return full_name


# имя
def user_firstname(user_id):
    data = pvk.users.get(
        user_ids=user_id,
        name_case='nom')
    firstname = data[0]['first_name']
    return firstname


# фамилия
def user_lastname(user_id):
    data = pvk.users.get(
        user_ids=user_id,
        name_case='nom')
    lastname = data[0]['last_name']
    return lastname


# поиск в вк
def user_search(sex, age_from, age_to, city_id=1):
    return pvk.users.search(
        can_write_private_message=1,
        count=1000,
        sex=sex,
        age_from=age_from,
        age_to=age_to,
        city=city_id,
        has_photo=1)


def photos_get():
    pvk.photos.get(owner_id='561548539', album_id='profile', extended=1)


# отбор 3 самых залайканых фотографии
def three_photos(index_in_open_users, user_data):
    photos = pvk.photos.get(
        owner_id=user_data[index_in_open_users][0],
        album_id='profile',
        extended=1)
    if photos['count'] >= 3:
        most_liked = {}
        three_photo_id = []
        for el in photos['items']:
            most_liked[el['id']] = el['likes']['count']
        sorted_photos = {k: v for k, v in sorted(most_liked.items(), key=lambda item: item[1])}
        for u_id in sorted_photos:
            three_photo_id.append(u_id)
        return (f'photo{user_data[index_in_open_users][0]}_{three_photo_id[-1]}',
                f'photo{user_data[index_in_open_users][0]}_{three_photo_id[-2]}',
                f'photo{user_data[index_in_open_users][0]}_{three_photo_id[-3]}')
    elif photos['count'] < 3:
        photo_id = pvk.users.get(
            user_ids=user_data[index_in_open_users][0],
            fields='photo_id')
        return f'photo{photo_id[0]["photo_id"]}'


# отправить сообщение
def msg_send(message, user_id, keyboard=None, attachment=None):
    vk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard,
        message=message,
        attachment=attachment)


# показать поп-ап сообщение
def show_pop_up(message, user_id, event):
    vk.messages.sendMessageEventAnswer(
        peer_id=event.object.peer_id,
        event_id=event.object.event_id,
        user_id=user_id,
        event_data=json.dumps({"type": "show_snackbar", "text": message}))


# изменить сообщение
def msg_edit(user_id, msg_id, message=None, keyboard=None, attachment=None):
    vk.messages.edit(
        peer_id=user_id,
        message=message,
        conversation_message_id=msg_id,
        keyboard=keyboard,
        attachment=attachment)


def main_func(user_id):
    """Основная логика программы.

    После получения первого сообщения от пользователя, вызывается цепочка
    линейных или ситуативных событий посредством event.object.payload.get('type').
    Типы payload заложен в каждой кнопке клавиатуры в файле keyboards.py
    Логика имеет 2 точки выхода - принудительную (когда пользователь жмет кнопку
    "завершить общение"), и ситуативную (когда поток сценария запущен и пользователь
    пишет сообщение боту). В иных случаях сценарий будет ожидать действий пользователя.

    """
    bot_users = session.query(BotUsers).get(user_id)
    params = session.query(SearchingParams).get(user_id)
    lmi = session.query(BotUsers.last_msg_id).where(BotUsers.vk_user_id == user_id)
    # слушаем события в потоке
    for event in longpoll.listen():
        # ситуативная точка выхода
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            session.query(OpenSearchData).filter(OpenSearchData.search_data_user_id == user_id).delete()
            bot_users.position = 0
            session.commit()
            return
        # если событие имеет тип "MESSAGE_REPLY" записываем id в БД
        if event.type == VkBotEventType.MESSAGE_REPLY:
            bot_users.last_msg_id = event.obj.conversation_message_id
            session.commit()
        # обрабатываем клики по callback кнопкам
        if event.type == VkBotEventType.MESSAGE_EVENT:
            # обработка линейных запросов
            if event.object.payload.get('type') == 'start_search':
                msg_send('С кем бы вы хотели познакомиться?', user_id, keyboard_2.get_keyboard())
            if event.object.payload.get('type') in SEX.keys():
                params.search_data_sex = SEX[event.object.payload.get('type')]
                msg_send('Какая возрастная категория Вас интересует?', user_id, keyboard_3.get_keyboard())
            if event.object.payload.get('type') in AGES.keys():
                params.search_data_age_from = AGES[event.object.payload.get('type')][0]
                params.search_data_age_to = AGES[event.object.payload.get('type')][1]
                session.commit()
                result = user_search(sex=params.search_data_sex,
                                     age_from=params.search_data_age_from,
                                     age_to=params.search_data_age_to,
                                     city_id=bot_users.city_id)['items']
                for user in result:
                    if not user['is_closed']:
                        session.add(OpenSearchData(search_user_id=user['id'],
                                                   search_data_user_id=user_id))
                        session.commit()
                data_len = session.query(func.count(OpenSearchData.search_user_id)). \
                    where(OpenSearchData.search_data_user_id == user_id).scalar()
                msg_send(f'Найдено {data_len} человек(а)!', user_id, keyboard_4.get_keyboard())
            oud = session.query(OpenSearchData.search_user_id). \
                where(OpenSearchData.search_data_user_id == user_id).all()
            if event.object.payload.get('type') == 'res':
                msg_send(
                    user_id=user_id,
                    message=(user_name(oud[bot_users.position][0]),
                             f'\nhttps://vk.com/id{oud[bot_users.position][0]}'),
                    keyboard=keyboard_6.get_keyboard(),
                    attachment=three_photos(bot_users.position, oud))
            if event.object.payload.get('type') == 'next':
                bot_users.position += 1
                session.commit()
                if bot_users.position in range(0, len(oud) - 1):
                    msg_edit(
                        user_id=user_id,
                        msg_id=lmi,
                        message=(user_name(oud[bot_users.position][0]),
                                 f'\nhttps://vk.com/id{oud[bot_users.position][0]}'),
                        keyboard=keyboard_5.get_keyboard(),
                        attachment=three_photos(bot_users.position, oud))
                else:
                    msg_edit(
                        user_id=user_id,
                        msg_id=lmi,
                        message=(user_name(oud[bot_users.position][0]),
                                 f'\nhttps://vk.com/id{oud[bot_users.position][0]}'),
                        keyboard=keyboard_7.get_keyboard(),
                        attachment=three_photos(bot_users.position, oud))
            if event.object.payload.get('type') == 'back':
                bot_users.position -= 1
                session.commit()
                if bot_users.position in range(1, len(oud) + 1):
                    msg_edit(user_id=user_id,
                             msg_id=lmi,
                             message=(user_name(oud[bot_users.position]),
                                      f'\nhttps://vk.com/id{oud[bot_users.position][0]}'),
                             keyboard=keyboard_5.get_keyboard(),
                             attachment=three_photos(bot_users.position, oud))
                elif bot_users.position == 0:
                    msg_edit(
                        user_id=user_id,
                        msg_id=lmi,
                        message=(user_name(oud[bot_users.position]), f'\nhttps://vk.com/id{oud[bot_users.position]}'),
                        keyboard=keyboard_6.get_keyboard(),
                        attachment=three_photos(bot_users.position, oud))
            # обработка ситуативных запросов
            if event.object.payload.get('type') == 'del_favorite':
                msg_send('Вы уверены?', user_id, keyboard_8.get_keyboard())
            if event.object.payload.get('type') == 'yes':
                session.query(Favorites).filter(Favorites.vk_user_id == user_id).delete()
                msg_edit(
                    message='Избранное очищено.',
                    user_id=user_id,
                    msg_id=lmi,
                    keyboard=keyboard_9.get_keyboard())
            if event.object.payload.get('type') == 'no':
                msg_edit(
                    user_id=user_id,
                    msg_id=lmi,
                    message=(user_name(oud[bot_users.position]), f'\nhttps://vk.com/id{oud[bot_users.position]}'),
                    keyboard=keyboard_6.get_keyboard(),
                    attachment=three_photos(bot_users.position, oud))
            if event.object.payload.get('type') == 'add_favorite':
                if not session.query(exists().where(Favorites.person_id == oud[bot_users.position][0])).scalar():
                    session.add(Favorites(vk_user_id=userid,
                                          person_id=oud[bot_users.position][0],
                                          first_name=user_firstname(oud[bot_users.position]),
                                          last_name=user_lastname(oud[bot_users.position]),
                                          link=f'https://vk.com/id{oud[bot_users.position][0]}'))
                    session.commit()
                    show_pop_up('Отличный выбор!', user_id, event)
                else:
                    show_pop_up('Пользователь уже в избранном.', user_id, event)
            if event.type == VkBotEventType.MESSAGE_EVENT:
                if event.object.payload.get('type') == 'show_favorite':
                    favor_query = session.query(Favorites.first_name, Favorites.last_name, Favorites.link). \
                        where(Favorites.vk_user_id == user_id).all()
                    favor_list = '\n'.join([f'{k + 1}) {v[0]} {v[1]} {v[2]}' for k, v in enumerate(favor_query)])
                    msg_send(
                        user_id=user_id,
                        message=f"Избранное:\n{favor_list}")
            if event.object.payload.get('type') == 'restart':
                session.query(OpenSearchData).filter(OpenSearchData.search_data_user_id == user_id).delete()
                bot_users.position = 0
                session.commit()
                msg_send('Вернул Вас в меню:', user_id, keyboard_9.get_keyboard())
            if event.object.payload.get('type') == 'end':
                session.query(OpenSearchData).filter(OpenSearchData.search_data_user_id == user_id).delete()
                bot_users.position = 0
                session.commit()
                msg_send(message='Я надеюсь, Вы нашли - то, что искали❤\n'
                                 'Если захотите снова пообщаться - напишите мне что-нибудь!😊',
                         user_id=user_id,
                         keyboard=keyboard_0
                         )
                return


if __name__ == '__main__':

    """Точка входа.

    Запуск сервера.
    Запуск бота.
    Прослушка событий в основном потоке программы.

    """

    # запускаем сервер в отдельном потоке для автополучения токена юзера (не реализовано)
    server_thread = threading.Thread(target=server_start, )
    server_thread.start()

    # запускаем бота
    vk_session = VkApi(token=group_token, api_version=API_VERSION)
    pvk_session = VkApi(token=personal_token, api_version=API_VERSION)
    vk = vk_session.get_api()
    pvk = pvk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    # слушаем ивенты в вк
    for new_event in longpoll.listen():
        if new_event.type == VkBotEventType.MESSAGE_NEW and new_event.from_user:
            userid = new_event.obj.message["from_id"]
            # если пользователь новый - заносим в БД
            if not session.query(exists().where(BotUsers.vk_user_id == userid)).scalar():
                msg_send(message='Привет! Меня зовут VkinderBot и я помогу найти Вам пару😍',
                         user_id=userid,
                         keyboard=keyboard_1.get_keyboard())
                session.add(BotUsers(vk_user_id=userid,
                                     first_name=user_firstname(userid),
                                     last_name=user_lastname(userid),
                                     city_id=user_city(userid),
                                     position=0))
                session.add(SearchingParams(search_params_user_id=userid))
                session.commit()
                thread = threading.Thread(target=main_func, args=(userid,))
                thread.start()
                print(f'Начинаем общение с пользователем id{userid}. Поток - {thread.name}')
            # если пользователь уже есть - отправляем ему главное меню
            else:
                msg_send(message=f'И снова здравствуйте, {user_firstname(userid)}! Кого ищем в этот раз?😋',
                         user_id=userid,
                         keyboard=keyboard_9.get_keyboard())
                thread = threading.Thread(target=main_func, args=(userid,))
                thread.start()
                print(f'Начинаем общение с пользователем id{userid}. Поток - {thread.name}')

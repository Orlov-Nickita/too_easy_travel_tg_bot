import telebot
import telegram
import re
import emoji
from loader import bot, search
from requests_rapidapiHotels import city_search, hotels_search_lowprice, photos_for_hotel
from keyboards import IKM_for_hotels_poisk, IKM_for_photos_search, IKM_for_greeting_msg, IKM_for_city_choice, \
    IKM_photos_sliding
from photo_album_class import Photo_album
from location_by_ip_address import ip_search


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая инициализирует поиск самых дешевых отелей. В рамках этой функции определяется местонахождение
    Пользователя и предлагается выбрать либо текущий город, либо другой желаемый.
    :param message: В качестве параметра передается сообщение Пользователя из бота, содержащее стартовую
    команду /lowprice
    :type message: telebot.types.Message
    :return: Выполняется обработка нажатия соответствующей кнопки клавиатуры.
    :rtype: None
    
    """
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    bot.send_message(chat_id = message.chat.id,
                     text = f'Ваше местоположение город {ip_search()}\n'
                            f'Хотите поменять город поиска или ищем по месту нахождения?',
                     reply_markup = IKM_for_greeting_msg()
                     )


@bot.callback_query_handler(func = lambda call: call.message.content_type == 'text'
                            and call.message.text.startswith('Ваше'))
def city_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_greeting_msg
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: В зависимости нажатой клавиши происходит переход либо к функции поиска совпадающих наименований городов,
    либо к функции ввода желаемого города для последующего поиска совпадающих наименований.
    :rtype: None
    """
    bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
    
    if call.data == ip_search():
        bot.answer_callback_query(callback_query_id = call.id, text = 'Принято')
        city_poisk(message = call.message, city = ip_search())
    
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = 'Принято')
        city_choice(message = call.message)


def city_choice(message: telebot.types.Message) -> None:
    """
    Функция, предназначенная для ввода желаемого отеля
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :return: После ввода города Пользователем значение передается в функцию city_poisk для поиска совпадений по
    введенному наименованию города.
    :rtype: None
    """
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    first_msg = bot.send_message(chat_id = message.chat.id, text = 'В каком городе будем искать отели?')
    
    bot.register_next_step_handler(message = first_msg, callback = city_poisk)


def city_poisk(message: telebot.types.Message, city = None) -> None:
    """
    Функция для нахождения совпадений по введенному наименованию города.
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :param city: В качестве параметра передается либо параметр нажатой кнопки callback_data, если Пользователь
    предпочел выполнить поиск исходя из его местоположения, либо параметр None, если Пользователь решил самостоятельно
    ввести название города, тогда наименование города будет содержаться в message.text
    :type city: None or str
    :return: Выводится клавиатура, содержащая наименования найденных городов близких по написанию (названию)
    к введенному, при нажатии на кнопки которой можно будет уточнить место поиска отелей.
    :rtype: None
    """
    search.found_cities = dict()
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    if city is not None:
        search.city = city
    else:
        search.city = message.text.title()
    
    msg = bot.send_message(chat_id = message.chat.id, text = f'Хороший выбор, ищу город {search.city} на карте')
    
    for group in city_search(msg, search.city)['suggestions']:
        if group['group'] == 'CITY_GROUP':
            for something in group['entities']:
                search.found_cities.update({re.sub(r"<span class='highlighted'>|</span>", '', something['caption']):
                                            int(something['destinationId'])
                                            }
                                           )
    
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    bot.delete_message(chat_id = msg.chat.id, message_id = msg.message_id)
    bot.send_message(chat_id = message.chat.id,
                     text = f'Вот, что мне удалось найти по запросу - город {search.city}\n'
                            f'Нажмите кнопку соответствующую Вашему запросу',
                     reply_markup = IKM_for_city_choice(search.found_cities)
                     )


@bot.callback_query_handler(func = lambda call: call.message.content_type == 'text'
                            and call.message.text.startswith('Вот'))
def city_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_city_choice
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши, содержащей название города
    :type call: telebot.types.CallbackQuery
    :return: Значение нажатой кнопки передается в функцию qty_hotels для определения желаемого количество отелей
    для поиска
    :rtype: None
    """
    if call.data == 'Back':
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = 'Выполняется поиск')
        bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
        search.city_id = call.data
        qty_hotels(message = call.message)


def qty_hotels(message: telebot.types.Message) -> None:
    """
    Функция для определения необходимого количество отелей для поиска
    :param message: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type message: telebot.types.Message
    :return: После выбора количество отелей информация передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    bot.send_message(chat_id = message.chat.id,
                     text = 'Итак, какое количество отелей подобрать?',
                     reply_markup = IKM_for_hotels_poisk()
                     )
    
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)


@bot.callback_query_handler(func = lambda call: call.message.content_type == 'text'
                            and call.message.text.startswith('Итак'))
def city_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_hotels_poisk
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей количество отелей
    :type call: call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    if call.data == 'Back':
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    
    bot.answer_callback_query(callback_query_id = call.id,
                              text = 'Выполняется поиск')
    bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
    hotels_poisk_in_the_city(message = call.message, hotels_qty = int(call.data), city_id = search.city_id)


def user_rating_false(hotel):  # Я пока не решил проблему отсутствия в некоторых местах тех или иных параметров.
    # Наверно для этих случаев надо мне сделать одну общую функцию, которая будет делать проверку ключей в словаре.
    # Пока так оставил эту и следующую
    try:
        hotel['guestReviews']
    except KeyError:
        return 'Нет оценок'
    else:
        return hotel['guestReviews']['unformattedRating']


def streetaddress_false(hotel):
    try:
        hotel['address']['streetAddress']
    except KeyError:
        return 'Нет адреса'
    else:
        return hotel['address']['streetAddress']


def hotels_poisk_in_the_city(message: telebot.types.Message, hotels_qty: int, city_id: int) -> None:
    """
    Функция, которая предназначена для сбора необходимой информации по необходимому количеству отелей в выбранном отеле
    :param message: В качестве параметра передается сообщение из чата с Пользователем
    :type message: telebot.types.Message
    :param hotels_qty: Передается количество отелей для поиска
    :type hotels_qty: int
    :param city_id: Передается id номер города, определенного ранее для поиска отелей в этом городе
    :type city_id:int
    :return: Для заданного количества отелей находится заранее определенная информация и упаковывается в словарь
    из словарей, который имеет следующий шаблон:
    {'Название отеля': {Информация по отелю}, 'Название отеля': {Информация по отелю}}
    Информация по отелю содержит в себе ID отеля, адрес, координаты, удаленность от центра, цену за 1 сутки, рейтинг
    отеля по мнению сайта, рейтинг отеля с точки зрения посетителей, ссылку на сайт.
    """
    search.hotels = dict()
    count = 0
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    
    for hotel in hotels_search_lowprice(message = message,
                                        city_destination_id = city_id)['data']['body']['searchResults']['results']:
        
        search.hotels.update({hotel['name']: {'ID отеля': hotel['id'],
                                              'Адрес': '{}, {}'.format(hotel['address']['locality'],
                                                                       streetaddress_false(hotel)),
                                              'Координаты': hotel['coordinate'],
                                              'Удаленность от центра': hotel['landmarks'][0]['distance'],
                                              'Цена': '{price} {days} {tax}'.format(
                                                  price = hotel['ratePlan']['price']['current'],
                                                  days = hotel['ratePlan']['price']['info'],
                                                  tax = hotel['ratePlan']['price']['summary']
                                              ),
                                              'Рейтинг отеля': '{stars} звезд{letter}'.format(
                                                  stars = hotel['starRating'],
                                                  letter = 'а' if hotel['starRating'] == 1
                                                  else 'ы'
                                              ),
                                              'Рейтинг по мнению посетителей': '{user_rating}'.format(
                                                  user_rating = user_rating_false(hotel)
                                              ),
                                              'Сайт': 'https://ru.hotels.com/ho{hotelid}'.format(
                                                  hotelid = hotel['id']
                                              )
                                              }
                              }
                             )
        
        count += 1
        
        if count == hotels_qty:
            break
    
    bot.send_message(chat_id = message.chat.id,
                     text = 'Потребуются ли фотографии для ознакомления?',
                     reply_markup = IKM_for_photos_search()
                     )


@bot.callback_query_handler(func = lambda call: call.message.content_type == 'text'
                            and call.message.text.startswith('Потребуются'))
def hotels_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки IKM_for_photos_search
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей ответ о
    необходимости фотографий
    :type call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_info
    :rtype: None
    """
    bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
    
    if call.data == 'Back':
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    
    bot.answer_callback_query(callback_query_id = call.id, text = 'Ответ принят')
    if call.data == 'Да':
        hotels_info(call.message, search.hotels, photo_need = True)
    
    if call.data == 'Нет':
        hotels_info(call.message, search.hotels, photo_need = False)
        

def yandex_maps(lat: int, long: int) -> str:
    """
    Функция, которая по имеющимся координатам формирует ссылку на Яндекс.карты
    :param lat: Передается широта
    :type lat: int
    :param long: Передается долгота
    :type long: int
    :return: Выводится строка, содержащая ссылку на Яндекс.карты
    :rtype: str
    """
    return f"https://maps.yandex.ru/?text={lat}+{long}"


def hotels_info(message: telebot.types.Message, found_hotels: dict, photo_need: bool) -> None:
    """
    Функция, которая выводит информацию по найденным отелям
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param found_hotels: В качестве параметра передается сформированный словарь с найденными отелями
    :type found_hotels: dict
    :param photo_need: В качестве параметра передается ответ о необходимости вывода фотографий
    :type photo_need: bool
    :return: Выводится сообщение ботом с информацией обо всех найденных отелях и фотоальбомом (опционально)
    :rtype: None
    """
    search.photos_dict = dict()
    search.photos_dict_urls = dict()
    for every_hotel in found_hotels:
        bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
        bot.send_message(chat_id = message.chat.id,
                         text = '{emoji1} Название отеля: <b>{hotel_name}</b>\n'
                                '{emoji2} Веб-сайт отеля: <a>{web}</a>\n'
                                '{emoji3} Адрес: <code>{address}</code>\n'
                                '{emoji4} Открыть Яндекс карты: <a>{yamaps}</a>\n'
                                '{emoji5} Удаленность от центра: <code>{center}</code>\n'
                                '{emoji6} Цена: <code>{price}</code>\n'
                                '{emoji7} Рейтинг: <code>{rating}</code>\n'
                                '{emoji8} Рейтинг по мнению посетителей: <code>{user_rating}</code>\n'.format(
            emoji1 = emoji.emojize(":hotel:", use_aliases = True),
            hotel_name = every_hotel,
            emoji2 = emoji.emojize(":globe_with_meridians:", use_aliases = True),
            web = found_hotels[every_hotel]['Сайт'],
            emoji3 = emoji.emojize(":earth_americas:", use_aliases = True),
            address = found_hotels[every_hotel]['Адрес'],
            emoji4 = emoji.emojize(":pushpin:", use_aliases = True),
            yamaps = yandex_maps(found_hotels[every_hotel]['Координаты']['lat'],
                                 found_hotels[every_hotel]['Координаты']['lon']
                                 ),
            emoji5 = emoji.emojize(":left_right_arrow:", use_aliases = True),
            center = found_hotels[every_hotel]['Удаленность от центра'],
            emoji6 = emoji.emojize(":credit_card:", use_aliases = True),
            price = found_hotels[every_hotel]['Цена'],
            emoji7 = emoji.emojize(":star:", use_aliases = True),
            rating = found_hotels[every_hotel]['Рейтинг отеля'],
            emoji8 = emoji.emojize(":sparkles:", use_aliases = True),
            user_rating = found_hotels[every_hotel]['Рейтинг по мнению посетителей'],
            ),
                         parse_mode = telegram.ParseMode.HTML,
                         )
        
        if photo_need:
            bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
            
            hotel_id = found_hotels[every_hotel]['ID отеля']
            hotel_photos = photos_for_hotel(message = message, hotel_id = hotel_id)
            search.photos_dict[hotel_id] = list()
            for every_photos in hotel_photos['hotelImages']:
                search.photos_dict[hotel_id].append(
                    every_photos['baseUrl'].format(size = every_photos['sizes'][0]['suffix']))
            
            all_photos = Photo_album(search.photos_dict[hotel_id])
            a = bot.send_photo(chat_id = message.chat.id, photo = str(all_photos), reply_markup = IKM_photos_sliding())
            search.photos_dict_urls.update({a.message_id: all_photos})


@bot.callback_query_handler(func = lambda call: call.message.content_type == 'photo')
def photo_slide(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_photos_sliding
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей направление
    прокрутки фотоальбома.
    :type call: telebot.types.CallbackQuery
    :return: При нажатии на кнопку меняется фотография.
    :rtype: None
    """
    if call.data == 'next':
        next_photo = search.photos_dict_urls[call.message.id].next()
        bot.edit_message_media(media = telebot.types.InputMedia(type = 'photo',
                                                                media = next_photo),
                               chat_id = call.message.chat.id,
                               message_id = call.message.message_id,
                               reply_markup = IKM_photos_sliding())
    if call.data == 'previous':
        next_photo = search.photos_dict_urls[call.message.id].prev()
        bot.edit_message_media(media = telebot.types.InputMedia(type = 'photo',
                                                                media = next_photo),
                               chat_id = call.message.chat.id,
                               message_id = call.message.message_id,
                               reply_markup = IKM_photos_sliding())

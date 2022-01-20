import telebot
import telegram
import re
import emoji
from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot, search
from requests_rapidapiHotels import city_search, hotels_search_price, photos_for_hotel
from keyboards import IKM_for_hotels_poisk, IKM_for_photos_search, IKM_for_greeting_msg, IKM_for_city_choice, \
    IKM_photos_sliding, IKM_date_chk_in_change, IKM_date_chk_out_change
from photo_album_class import Photo_album
from location_by_ip_address import ip_search
import logging
from auxiliary_functions import date_change, yandex_maps, user_rating_false, streetaddress_false, info_check, \
    summary_check, button_text


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
    logging.info('Запущена функция start с определением местоположения Пользователя')
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    cur_city = ip_search()
    logging.info(f'Бот определил местоположение Пользователя в городе "{cur_city}"')
    msg = bot.send_message(chat_id = message.chat.id,
                           text = f'Ваше местоположение город {cur_city}. '
                                  f'Хотите поменять город поиска или ищем по месту нахождения?',
                           reply_markup = IKM_for_greeting_msg()
                           )
    logging.info(f'Бот отправил сообщение "{msg.text}"')


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
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}" и выбрал текущее местоположение')
        bot.answer_callback_query(callback_query_id = call.id, text = 'Принято')
        city_poisk(message = call.message, city = ip_search())
    
    else:
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}" и предпочел выбрать другой город для поиска')
        bot.answer_callback_query(callback_query_id = call.id, text = 'Принято')
        city_choice(message = call.message)


def city_choice(message: telebot.types.Message) -> None:
    """
    Функция, предназначенная для ввода желаемого города
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :return: После ввода города Пользователем значение передается в функцию city_poisk для поиска совпадений по
    введенному наименованию города.
    :rtype: None
    """
    
    logging.info('Запущена функция city_choice')
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    first_msg = bot.send_message(chat_id = message.chat.id, text = 'В каком городе будем искать отели?')
    logging.info(f'Бот отправил сообщение "{first_msg.text}"')
    
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
    logging.info('Запущена функция city_poisk')
    
    search.found_cities = dict()
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    if city is not None:
        search.city = city
    else:
        search.city = message.text.title()
    
    msg = bot.send_message(chat_id = message.chat.id, text = f'Хороший выбор, ищу город {search.city} на карте')
    logging.info(f'Бот отправил сообщение "{msg.text}"')
    
    for group in city_search(msg, search.city)['suggestions']:
        if group['group'] == 'CITY_GROUP':
            for something in group['entities']:
                search.found_cities.update({re.sub(r"<span class='highlighted'>|</span>", '', something['caption']):
                                                int(something['destinationId'])
                                            }
                                           )
    
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    bot.delete_message(chat_id = msg.chat.id, message_id = msg.message_id)
    
    msg2 = bot.send_message(chat_id = message.chat.id,
                            text = f'Вот, что мне удалось найти по запросу - город {search.city} '
                                   f'Нажмите кнопку соответствующую Вашему запросу',
                            reply_markup = IKM_for_city_choice(search.found_cities)
                            )
    logging.info(f'Бот отправил сообщение "{msg2.text}", {search.found_cities}')


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
    logging.info(f'Пользователь выбрал место поиска "{button_text(call)}"')
    logging.info('Запущена функция city_choice_keyboard_callback')
    if call.data == 'Back':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    else:
        bot.answer_callback_query(callback_query_id = call.id, text = 'Выполняется поиск')
        bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
        search.city_id = call.data
        check_in_date_choice(call.message)


def check_in_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты въезда в отель через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logging.info('Запущена функция check_in_date_choice')
    
    calendar, step = DetailedTelegramCalendar(calendar_id = 1, locale = 'ru').build()
    msg = bot.send_message(chat_id = message.chat.id,
                           text = "Выберите дату въезда",
                           reply_markup = calendar)
    logging.info(f'Бот отправил сообщение "{msg.text}"')


@bot.callback_query_handler(func = DetailedTelegramCalendar.func(calendar_id = 1))
def chk_in_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logging.info('Запущена функция chk_in_date_calendar')
    
    result, key, step = DetailedTelegramCalendar(calendar_id = 1, locale = 'ru').process(c.data)
    if not result and key:
        bot.edit_message_text("Выберите дату въезда",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup = key)
    elif result:
        search.check_in = result
        bot.edit_message_text(f'Вы выбрали дату въезда {date_change(result)}', c.message.chat.id,
                              c.message.message_id, reply_markup = IKM_date_chk_in_change())
        logging.info(f'Пользователь выбрал дату въезда {search.check_in}')


@bot.callback_query_handler(
    func = lambda call: call.message.content_type == 'text' and call.message.text.startswith('Вы выбрали дату въезда'))
def chk_in_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info('Запущена функция chk_in_date_change')
    
    if call.data == 'cancel':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        check_in_date_choice(call.message)
    
    elif call.data == 'continue':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        check_out_date_choice(call.message)


def check_out_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты выезда из отеля через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logging.info('Запущена функция check_out_date_choice')
    
    calendar, step = DetailedTelegramCalendar(calendar_id = 2, locale = 'ru').build()
    msg = bot.send_message(chat_id = message.chat.id,
                           text = "Выберите дату выезда",
                           reply_markup = calendar)
    logging.info(f'Бот отправил сообщение "{msg.text}"')


@bot.callback_query_handler(func = DetailedTelegramCalendar.func(calendar_id = 2))
def chk_out_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logging.info('Запущена функция check_out_date_choice')
    
    result, key, step = DetailedTelegramCalendar(calendar_id = 2, locale = 'ru').process(c.data)
    if not result and key:
        bot.edit_message_text("Выберите дату выезда",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup = key)
    elif result:
        if result == search.check_in:
            bot.answer_callback_query(callback_query_id = c.id,
                                      text = 'Дата выезда не может совпадать с датой въезда. Минимальный срок '
                                             'бронирования отеля составляет 1 сутки. Пожалуйста, выберите дату выезда '
                                             'еще раз',
                                      show_alert = True)
            logging.info(f'Пользователь выбрал дату выезда {date_change(result)} такую же как дату въезда. Бот включил '
                         f'уведомление об ошибке')
            bot.delete_message(c.message.chat.id, c.message.message_id)
            
            check_out_date_choice(c.message)
        else:
            search.check_out = result
            bot.edit_message_text(f'Вы выбрали дату выезда {date_change(result)}', c.message.chat.id,
                                  c.message.message_id, reply_markup = IKM_date_chk_out_change())
            logging.info(f'Пользователь выбрал дату выезда {search.check_out}')


@bot.callback_query_handler(
    func = lambda call: call.message.content_type == 'text' and call.message.text.startswith('Вы выбрали дату выезда'))
def chk_out_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info('Запущена функция chk_out_date_change')
    
    if call.data == 'cancel':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        check_out_date_choice(call.message)
    
    elif call.data == 'continue':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        qty_hotels(call.message)


def qty_hotels(message: telebot.types.Message) -> None:
    """
    Функция для определения необходимого количество отелей для поиска
    :param message: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type message: telebot.types.Message
    :return: После выбора количество отелей информация передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    logging.info('Запущена функция qty_hotels')
    
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id = message.chat.id,
                           text = 'Итак, какое количество отелей подобрать?',
                           reply_markup = IKM_for_hotels_poisk()
                           )
    logging.info(f'Бот отправил сообщение "{msg.text}"')
    
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
    logging.info('Запущена функция city_poisk_keyboard_callback')
    
    if call.data == 'Back':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    
    else:
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.answer_callback_query(callback_query_id = call.id,
                                  text = 'Выполняется поиск')
        bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
        hotels_poisk_in_the_city(message = call.message, hotels_qty = int(call.data))


def hotels_poisk_in_the_city(message: telebot.types.Message, hotels_qty: int) -> None:
    """
    Функция, которая предназначена для сбора необходимой информации по необходимому количеству отелей в выбранном отеле
    :param message: В качестве параметра передается сообщение из чата с Пользователем
    :type message: telebot.types.Message
    :param hotels_qty: Передается количество отелей для поиска
    :type hotels_qty: int
    :return: Для заданного количества отелей находится заранее определенная информация и упаковывается в словарь
    из словарей, который имеет следующий шаблон:
    {'Название отеля': {Информация по отелю}, 'Название отеля': {Информация по отелю}}
    Информация по отелю содержит в себе ID отеля, адрес, координаты, удаленность от центра, цену за 1 сутки, рейтинг
    отеля по мнению сайта, рейтинг отеля с точки зрения посетителей, ссылку на сайт.
    """
    logging.info('Запущена функция hotels_poisk_in_the_city')
    
    search.hotels = dict()
    count = 0
    bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
    
    for hotel in \
            hotels_search_price(message = message,
                                city_destination_id = search.city_id,
                                chk_in = search.check_in,
                                chk_out = search.check_out,
                                sort_price = 'PRICE'
                                )['data']['body']['searchResults']['results']:
        
        search.hotels.update({hotel['name']: {
            'ID отеля': hotel['id'],
            'Адрес': '{}, {}'.format(hotel['address']['locality'],
                                     streetaddress_false(hotel)),
            'Координаты': hotel['coordinate'],
            'Удаленность от центра': hotel['landmarks'][0]['distance'],
            'Цена за весь период': '{price} {days} {tax}'.format(
                price = hotel['ratePlan']['price']['current'],
                days = info_check(hotel),
                tax = summary_check(hotel)
            ),
            'Цена за 1 сутки': int(
                hotel['ratePlan']['price']['exactCurrent'] // (search.check_out.day - search.check_in.day)
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
    
    msg = bot.send_message(chat_id = message.chat.id,
                           text = 'Потребуются ли фотографии для ознакомления?',
                           reply_markup = IKM_for_photos_search()
                           )
    logging.info(f'Бот отправил сообщение "{msg.text}"')


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
    logging.info('Запущена функция hotels_poisk_keyboard_callback')
    
    bot.send_chat_action(chat_id = call.message.chat.id, action = telegram.ChatAction.TYPING)
    
    if call.data == 'Back':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    
    bot.answer_callback_query(callback_query_id = call.id, text = 'Ответ принят')
    
    if call.data == 'Да':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        hotels_info(call.message, search.hotels, photo_need = True)
    
    if call.data == 'Нет':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        hotels_info(call.message, search.hotels, photo_need = False)


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
    logging.info('Запущена функция hotels_info')
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
                                '{emoji6} Цена за весь период: <code>{price}</code>\n'
                                '{emoji7} Дата въезда: <code>{chk_in_date}</code>\n'
                                '{emoji8} Дата выезда: <code>{chk_out_date}</code>\n'
                                '{emoji9} Цена за сутки: <code>{one_day_price}</code>\n'
                                '{emoji10} Рейтинг: <code>{rating}</code>\n'
                                '{emoji11} Рейтинг по мнению посетителей: <code>{user_rating}</code>\n'.format(
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
                             price = found_hotels[every_hotel]['Цена за весь период'],
                             emoji7 = emoji.emojize(":soon:", use_aliases = True),
                             emoji8 = emoji.emojize(":back:", use_aliases = True),
                             chk_in_date = date_change(search.check_in),
                             chk_out_date = date_change(search.check_out),
                             emoji9 = emoji.emojize(":one:", use_aliases = True),
                             one_day_price = '{0:,} RUB'.format(found_hotels[every_hotel]['Цена за 1 сутки']),
                             emoji10 = emoji.emojize(":star:", use_aliases = True),
                             rating = found_hotels[every_hotel]['Рейтинг отеля'],
                             emoji11 = emoji.emojize(":sparkles:", use_aliases = True),
                             user_rating = found_hotels[every_hotel]['Рейтинг по мнению посетителей'],
                         ),
                         parse_mode = telegram.ParseMode.HTML,
                         disable_web_page_preview = True
                         )
        logging.info(f'Бот отправил сообщение c информацией по отелю')
        
        if photo_need:
            bot.send_chat_action(chat_id = message.chat.id, action = telegram.ChatAction.TYPING)
            
            hotel_id = found_hotels[every_hotel]['ID отеля']
            """
            В рамках общего цикла, где мы перебираем все отели от 1 до выбранного Пользователя, мы сохраняем
            значение ID каждого из этих отелей в переменную
            """
            hotel_photos = photos_for_hotel(message = message, hotel_id = hotel_id)
            """
            Получив ранее ID отеля, мы обращаемся к функции hotel_photos для того чтобы получить JSON ответ,
            содержащий фотографии отеля
            """
            search.photos_dict[hotel_id] = list()
            """
            В экземпляре класса User_search в аттрибуте photos_dict создается пустой список, в который далее мы
            сохраним все имеющиеся фотографии в виде ссылок
            """
            for every_photos in hotel_photos['hotelImages']:
                """
                Циклом проходим по всем имеющимся фотографиям в JSON ответе с сервера
                """
                search.photos_dict[hotel_id].append(
                    every_photos['baseUrl'].format(size = every_photos['sizes'][0]['suffix']))
                """
                А теперь в аттрибут photos_dict, где создан пустой список, добавляем все ссылки циклом, так как они все
                лежат в определенных местах независимо друг от друга
                """
            
            all_photos = Photo_album(search.photos_dict[hotel_id])
            """
            Создаем экземпляр класса Photo_album, который превращает обычный список в итерируемый в обе стороны.
            Используя понятные методы next и prev мы можем вращать список на 1 единицу, получая тем самым доступ к
            текущему, следующему и предыдущему объекту в списке. И используя команду send_photo отправляем первую
            имеющуюся в списке фотографию в чат бота
            """
            a = bot.send_photo(chat_id = message.chat.id, photo = str(all_photos), reply_markup = IKM_photos_sliding())
            """
            Сохраняем в переменную отправленное сообщение, чтобы иметь возможность созданный ранее список с новыми
            функциями присвоить в словаре ключу содержащий ID сообщения. Это позволит нам идентифицировать каждое
            нажатие пользователя. У клавиатуры и сообщения, под которым появляется клавиатура, идентификаторы сообщения
            одинаковые, а значит это позволяет нам менять именно то фото, под которым была нажата кнопка, так как
            call.message.id (в следующем обработчике) и a.message.id одинаковые.
            """
            search.photos_dict_urls.update({a.message_id: all_photos})
            logging.info(f'Бот отправил сообщение фото')


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
    logging.info('Запущена функция photo_slide - открыта клавиатура')
    
    if call.data == 'next':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        
        next_photo = search.photos_dict_urls[call.message.id].next()
        bot.edit_message_media(media = telebot.types.InputMedia(type = 'photo',
                                                                media = next_photo),
                               chat_id = call.message.chat.id,
                               message_id = call.message.message_id,
                               reply_markup = IKM_photos_sliding())
    
    if call.data == 'previous':
        logging.info(f'Пользователь нажал на кнопку "{button_text(call)}"')
        
        next_photo = search.photos_dict_urls[call.message.id].prev()
        bot.edit_message_media(media = telebot.types.InputMedia(type = 'photo',
                                                                media = next_photo),
                               chat_id = call.message.chat.id,
                               message_id = call.message.message_id,
                               reply_markup = IKM_photos_sliding())

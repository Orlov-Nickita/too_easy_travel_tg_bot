import telebot
import telegram
import re
import emoji
from telegram_bot_calendar import DetailedTelegramCalendar
from my_bot.loader import bot, search
from commands_and_keyboards.keyboards import IKM_price_distance_approve
from utils.errors import Negative_value, Max_more_min
from utils.sqlite import data_add
from useful_add_func.requests_rapidapiHotels import city_search, hotels_search_price, photos_for_hotel
from commands_and_keyboards.keyboards import IKM_for_hotels_poisk, IKM_for_photos_search, IKM_for_greeting_msg, \
    IKM_for_city_choice, IKM_photos_sliding, IKM_date_chk_in_change, IKM_date_chk_out_change
from useful_add_func.photo_album_class import Photo_album
from useful_add_func.location_by_ip_address import ip_search
import logging
from useful_add_func.auxiliary_functions import date_change, yandex_maps, user_rating_false, streetaddress_false, \
    info_check, \
    summary_check, button_text
from datetime import date
from dateutil.relativedelta import relativedelta
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая инициализирует поиск самых дешевых отелей. В рамках этой функции определяется местонахождение
    Пользователя и предлагается выбрать либо текущий город, либо другой желаемый.
    :param message: В качестве параметра передается сообщение Пользователя из бота, содержащее стартовую
    команду /command
    :type message: telebot.types.Message
    :return: Выполняется обработка нажатия соответствующей кнопки клавиатуры.
    :rtype: None

    """
    logging.info(lang_dict[search.lang]['command_logging']['log1'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    cur_city = ip_search()
    logging.info(lang_dict[search.lang]['command_logging']['log2'].format(city=cur_city), extra=search.user_id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text1'].format(city=cur_city),
                           reply_markup=IKM_for_greeting_msg()
                           )
    logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[search.lang]['command']['text1.1']))
def city_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_greeting_msg
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: В зависимости нажатой клавиши происходит переход либо к функции поиска совпадающих наименований городов,
    либо к функции ввода желаемого города для последующего поиска совпадающих наименований.
    :rtype: None
    """
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    if call.data == ip_search():
        logging.info(lang_dict[search.lang]['command_logging']['log4'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.answer_callback_query(callback_query_id=call.id, text=lang_dict[search.lang]['command_acq']['acq1'])
        city_poisk(message=call.message, city=ip_search())
    
    else:
        logging.info(lang_dict[search.lang]['command_logging']['log5'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.answer_callback_query(callback_query_id=call.id, text=lang_dict[search.lang]['command_acq']['acq1'])
        city_choice(message=call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def city_choice(message: telebot.types.Message) -> None:
    """
    Функция, предназначенная для ввода желаемого города
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :return: После ввода города Пользователем значение передается в функцию city_poisk для поиска совпадений по
    введенному наименованию города.
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['command_logging']['log6'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    first_msg = bot.send_message(chat_id=message.chat.id,
                                 text=lang_dict[search.lang]['command']['text2'])
    logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=first_msg.text), extra=search.user_id)
    
    bot.register_next_step_handler(message=first_msg, callback=city_poisk)


def city_poisk(message: telebot.types.Message, city=None) -> None:
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
    logging.info(lang_dict[search.lang]['command_logging']['log8'], extra=search.user_id)
    
    search.found_cities = dict()
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    if city is not None:
        search.city = city
    else:
        search.city = message.text.title()
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text3'].format(city=search.city))
    logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)
    
    for group in city_search(
            message=msg, locale=search.locale, city_name=search.city, currency=search.currency)['suggestions']:
        if group['group'] == 'CITY_GROUP':
            for something in group['entities']:
                search.found_cities.update({re.sub(r"<span class='highlighted'>|</span>", '',
                                                   something['caption']): int(something['destinationId'])})
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    
    msg2 = bot.send_message(chat_id=message.chat.id,
                            text=lang_dict[search.lang]['command']['text4'].format(city=search.city),
                            reply_markup=IKM_for_city_choice(search.found_cities)
                            )
    logging.info(lang_dict[search.lang]['command_logging']['log9'].format(msg2=msg2.text, cities=search.found_cities),
                 extra=search.user_id)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[search.lang]['command']['text4.1']))
def city_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_city_choice
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши, содержащей название города
    :type call: telebot.types.CallbackQuery
    :return: Значение нажатой кнопки передается в функцию qty_hotels для определения желаемого количество отелей
    для поиска
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log10'].format(button=button_text(call)),
                 extra=search.user_id)
    logging.info(lang_dict[search.lang]['command_logging']['log11'], extra=search.user_id)

    bot.answer_callback_query(callback_query_id=call.id, text=lang_dict[search.lang]['command_acq']['acq2'])
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    search.city_id = call.data
    
    check_in_date_choice(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def check_in_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты въезда в отель через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log12'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              locale=search.lang,
                                              min_date=date.today(),
                                              max_date=date.today() + relativedelta(months=2)).build()
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text5'],
                           reply_markup=calendar)
    logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def chk_in_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log13'], extra=search.user_id)
    
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale=search.lang,
                                                 min_date=date.today(),
                                                 max_date=date.today() + relativedelta(months=2)).process(c.data)
    if not result and key:
        bot.edit_message_text(text=lang_dict[search.lang]['command']['text5'],
                              chat_id=c.message.chat.id,
                              message_id=c.message.message_id,
                              reply_markup=key)
    elif result:
        search.check_in = result
        bot.edit_message_text(text=lang_dict[search.lang]['command']['text6'].format(res=date_change(result)),
                              chat_id=c.message.chat.id,
                              message_id=c.message.message_id,
                              reply_markup=IKM_date_chk_in_change()
                              )
        logging.info(lang_dict[search.lang]['command_logging']['log14'].format(time_res=search.check_in),
                     extra=search.user_id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[search.lang]['command']['text6.1']))
def chk_in_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log15'], extra=search.user_id)
    
    if call.data == 'cancel':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        check_in_date_choice(call.message)
    
    elif call.data == 'continue':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        check_out_date_choice(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def check_out_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты выезда из отеля через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log17'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                              locale=search.lang,
                                              min_date=search.check_in + relativedelta(days=1),
                                              max_date=search.check_in + relativedelta(months=2)).build()
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text7'],
                           reply_markup=calendar)
    logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def chk_out_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log18'], extra=search.user_id)
    
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 locale=search.lang,
                                                 min_date=search.check_in + relativedelta(days=1),
                                                 max_date=search.check_in + relativedelta(months=2)).process(c.data)
    if not result and key:
        bot.edit_message_text(text=lang_dict[search.lang]['command']['text7'],
                              chat_id=c.message.chat.id,
                              message_id=c.message.message_id,
                              reply_markup=key)
    elif result:
        if result == search.check_in:
            bot.answer_callback_query(callback_query_id=c.id,
                                      text=lang_dict[search.lang]['command']['text9'],
                                      show_alert=True)
            logging.info(lang_dict[search.lang]['command_logging']['log19'].format(time_res=date_change(result)),
                         extra=search.user_id)
            bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
            
            check_out_date_choice(c.message)
        else:
            search.check_out = result
            bot.edit_message_text(text=lang_dict[search.lang]['command']['text8'].format(res=date_change(result)),
                                  chat_id=c.message.chat.id,
                                  message_id=c.message.message_id,
                                  reply_markup=IKM_date_chk_out_change())
            logging.info(lang_dict[search.lang]['command_logging']['log20'].format(time_res=search.check_out),
                         extra=search.user_id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[search.lang]['command']['text8.1']))
def chk_out_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log21'], extra=search.user_id)
    
    if call.data == 'cancel':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        check_out_date_choice(call.message)
    
    elif call.data == 'continue':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        
        if search.sort == 'DISTANCE_FROM_LANDMARK':
            price_range(call.message)
        else:
            qty_hotels(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def price_range(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['command_logging']['log30'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text13'])
    logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
    
    bot.register_next_step_handler(message=msg, callback=price_limiter)


def price_limiter(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['command_logging']['log41'].format(msg=message.text), extra=search.user_id)
    logging.info(lang_dict[search.lang]['command_logging']['log31'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    try:
        search.min_price, search.max_price = int(message.text.split()[0]), int(message.text.split()[1])
        
        if search.max_price <= search.min_price:
            raise Max_more_min
        
        elif search.min_price < 0 or search.max_price < 0:
            raise Negative_value
    
    except IndexError as Ex:
        logging.info(lang_dict[search.lang]['command_logging']['log37'], extra=search.user_id)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text18'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        logging.info(lang_dict[search.lang]['command_logging']['log38'].format(Ex), extra=search.user_id)
        price_range(message=message)
    
    except Negative_value:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text20'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        price_range(message=message)
    
    except Max_more_min:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text21'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        price_range(message=message)
    
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text22'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        price_range(message=message)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text15'].format(search.min_price,
                                                                                       search.max_price),
                               reply_markup=IKM_price_distance_approve())
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[search.lang]['command']['text15.1']))
def price_limiter_approve(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение расстояния, либо переход к
    следующему шагу - количество отелей
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log34'], extra=search.user_id)
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    if call.data == 'cancel':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        price_range(call.message)
    
    elif call.data == 'continue':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        distance_range(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def distance_range(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['command_logging']['log32'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text14'])
    logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
    
    bot.register_next_step_handler(message=msg, callback=distance_limiter)


def distance_limiter(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['command_logging']['log41'].format(msg=message.text), extra=search.user_id)
    logging.info(lang_dict[search.lang]['command_logging']['log33'], extra=search.user_id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    try:
        search.min_dist, search.max_dist = int(message.text.split()[0]), int(message.text.split()[1])
    
    except IndexError as Ex:
        
        logging.info(lang_dict[search.lang]['command_logging']['log39'], extra=search.user_id)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text19'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        logging.info(lang_dict[search.lang]['command_logging']['log40'].format(Ex), extra=search.user_id)
        distance_range(message=message)
    
    except Negative_value:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text23'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        distance_range(message=message)
    
    except Max_more_min:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text24'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        distance_range(message=message)
    
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text22'])
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)
        distance_range(message=message)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['command']['text16'].format(search.min_dist,
                                                                                       search.max_dist),
                               reply_markup=IKM_price_distance_approve())
        logging.info(lang_dict[search.lang]['command_logging']['log7'].format(msg=msg.text), extra=search.user_id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[search.lang]['command']['text16.1'].format(search.min_dist, search.max_dist)))
def distance_limiter_approve(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение цен, либо переход к
    следующему шагу - выбору диапозона расстояния
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log35'], extra=search.user_id)
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    if call.data == 'cancel':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        distance_range(call.message)
    
    elif call.data == 'continue':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        qty_hotels(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def qty_hotels(message: telebot.types.Message) -> None:
    """
    Функция для определения необходимого количество отелей для поиска
    :param message: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type message: telebot.types.Message
    :return: После выбора количество отелей информация передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log22'], extra=search.user_id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['command']['text10'],
                           reply_markup=IKM_for_hotels_poisk()
                           )
    logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[search.lang]['command']['text10']))
def city_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_hotels_poisk
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей количество отелей
    :type call: call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['command_logging']['log23'], extra=search.user_id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    

    logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                 extra=search.user_id)
    bot.answer_callback_query(callback_query_id=call.id,
                              text=lang_dict[search.lang]['command_acq']['acq2'])
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    search.hotels_qty = int(call.data)
    hotels_poisk_in_the_city(message=call.message, hotels_qty=search.hotels_qty)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.edit_message_text(text=lang_dict[search.lang]['command']['text25'].format(button=button_text(call)),
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          parse_mode=telegram.ParseMode.HTML)


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
    logging.info(lang_dict[search.lang]['command_logging']['log24'], extra=search.user_id)
    
    search.hotels = dict()
    count = 0
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    while True:
        for hotel in \
                hotels_search_price(message=message,
                                    city_destination_id=search.city_id,
                                    pagenumber=search.pagenumber,
                                    chk_in=search.check_in,
                                    chk_out=search.check_out,
                                    min_price=search.min_price,
                                    max_price=search.max_price,
                                    sort=search.sort,
                                    locale=search.locale,
                                    currency=search.currency
                                    )['data']['body']['searchResults']['results']:
            
            bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
            logging.info(lang_dict[search.lang]['command_logging']['log36'].format(search.pagenumber),
                         extra=search.user_id)
            landmark_distance = float(hotel['landmarks'][0]['distance'].split()[0].replace(',', '.')) * 1000
            
            if search.sort == 'DISTANCE_FROM_LANDMARK' and (
                    landmark_distance >= search.max_dist or landmark_distance <= search.min_dist):
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                continue
            
            else:
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                search.hotels.update({hotel['name']: {
                    lang_dict[search.lang]['command_print_search_info']['key1']: hotel['id'],
                    lang_dict[search.lang]['command_print_search_info']['key2']: '{}, {}'.format(
                        hotel['address']['locality'],
                        streetaddress_false(hotel)),
                    lang_dict[search.lang]['command_print_search_info']['key3']: hotel['coordinate'],
                    lang_dict[search.lang]['command_print_search_info']['key4']: hotel['landmarks'][0]['distance'],
                    lang_dict[search.lang]['command_print_search_info']['key5']: '{price} {days} {tax}'.format(
                        price=hotel['ratePlan']['price']['current'],
                        days=info_check(hotel),
                        tax=summary_check(hotel)
                    ),
                    lang_dict[search.lang]['command_print_search_info']['key6']: int(
                        hotel['ratePlan']['price']['exactCurrent'] / int(
                            str(search.check_out - search.check_in).split()[0])
                    ),
                    lang_dict[search.lang]['command_print_search_info']['key7']: '{stars} звезд{letter}'.format(
                        stars=hotel['starRating'],
                        letter='а' if hotel['starRating'] == 1
                        else 'ы'
                    ),
                    lang_dict[search.lang]['command_print_search_info']['key8']: '{user_rating}'.format(
                        user_rating=user_rating_false(hotel)),
                    lang_dict[search.lang]['command_print_search_info'][
                        'key9']: 'https://ru.hotels.com/ho{hotelid}'.format(
                        hotelid=hotel['id'])
                }
                }
                )
                count += 1
                if count == hotels_qty:
                    break
        
        if count == hotels_qty:
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=lang_dict[search.lang]['command']['text11'],
                                   reply_markup=IKM_for_photos_search()
                                   )
            logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text), extra=search.user_id)
            break
        else:
            search.pagenumber += 1
            
            if search.pagenumber == 4:
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                msg = bot.send_message(chat_id=message.chat.id,
                                       text=lang_dict[search.lang]['command']['text17'])
                logging.info(lang_dict[search.lang]['command_logging']['log3'].format(msg=msg.text),
                             extra=search.user_id)
                search.pagenumber = 1
                price_range(message=message)
                break


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[search.lang]['command']['text11']))
def hotels_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки IKM_for_photos_search
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей ответ о
    необходимости фотографий
    :type call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_info
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['command_logging']['log25'], extra=search.user_id)
    
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    bot.answer_callback_query(callback_query_id=call.id, text=lang_dict[search.lang]['command_acq']['acq3'])
    
    if call.data == 'Yes':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        hotels_info(call.message, search.hotels, photo_need=True)
    
    if call.data == 'No':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        hotels_info(call.message, search.hotels, photo_need=False)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.edit_message_text(text=lang_dict[search.lang]['command']['text26'].format(button=button_text(call)),
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          parse_mode=telegram.ParseMode.HTML)


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
    logging.info(lang_dict[search.lang]['command_logging']['log26'], extra=search.user_id)
    search.photos_dict = dict()
    search.photos_dict_urls = dict()
    for every_hotel in found_hotels:
        bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
        msg_info = bot.send_message(chat_id=message.chat.id,
                                    text=lang_dict[search.lang]['command']['text12'].format(
                                        emoji1=emoji.emojize(":hotel:", use_aliases=True),
                                        hotel_name=every_hotel,
                                        emoji2=emoji.emojize(":globe_with_meridians:", use_aliases=True),
                                        web=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key9']],
                                        emoji3=emoji.emojize(":earth_americas:", use_aliases=True),
                                        address=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key2']],
                                        emoji4=emoji.emojize(":pushpin:", use_aliases=True),
                                        yamaps=yandex_maps(found_hotels[every_hotel][
                                                               lang_dict[search.lang]['command_print_search_info'][
                                                                   'key3']][
                                                               'lat'],
                                                           found_hotels[every_hotel][
                                                               lang_dict[search.lang]['command_print_search_info'][
                                                                   'key3']]['lon']
                                                           ),
                                        emoji5=emoji.emojize(":left_right_arrow:", use_aliases=True),
                                        center=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key4']],
                                        emoji6=emoji.emojize(":credit_card:", use_aliases=True),
                                        price=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key5']],
                                        emoji7=emoji.emojize(":soon:", use_aliases=True),
                                        emoji8=emoji.emojize(":back:", use_aliases=True),
                                        chk_in_date=date_change(search.check_in),
                                        chk_out_date=date_change(search.check_out),
                                        emoji9=emoji.emojize(":one:", use_aliases=True),
                                        one_day_price='{0:,} {cur}'.format(
                                            found_hotels[every_hotel][lang_dict[search.lang][
                                                'command_print_search_info']['key6']],
                                            cur=search.currency),
                                        emoji10=emoji.emojize(":star:", use_aliases=True),
                                        rating=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key7']],
                                        emoji11=emoji.emojize(":sparkles:", use_aliases=True),
                                        user_rating=found_hotels[every_hotel][
                                            lang_dict[search.lang]['command_print_search_info']['key8']],
                                    ),
                                    parse_mode=telegram.ParseMode.HTML,
                                    disable_web_page_preview=True
                                    )
        logging.info(lang_dict[search.lang]['command_logging']['log27'], extra=search.user_id)
        data_add(sql_base='user_database.db', user_id=message.chat.id,
                 message_id=msg_info.message_id, msg_content='hotel_information_message')
        
        if photo_need:
            bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
            
            hotel_id = found_hotels[every_hotel][lang_dict[search.lang]['command_print_search_info']['key1']]
            """
            В рамках общего цикла, где мы перебираем все отели от 1 до выбранного количества Пользователем, мы сохраняем
            значение ID каждого из этих отелей в переменную
            """
            hotel_photos = photos_for_hotel(message=message, hotel_id=hotel_id)
            """
            Получив ранее ID отеля, мы обращаемся к функции photos_for_hotel для того чтобы получить JSON ответ,
            содержащий фотографии отеля
            """
            search.photos_dict[hotel_id] = list()
            """
            В экземпляре класса User_search в атрибуте photos_dict создается пустой список, в который далее мы
            сохраним все имеющиеся фотографии в виде ссылок
            """
            for every_photos in hotel_photos['hotelImages']:
                """
                Циклом проходим по всем имеющимся фотографиям в JSON ответе с сервера
                """
                search.photos_dict[hotel_id].append(
                    every_photos['baseUrl'].format(size=every_photos['sizes'][0]['suffix']))
                """
                А теперь в атрибут photos_dict, где создан пустой список, добавляем все ссылки циклом, так как они все
                лежат в определенных местах независимо друг от друга
                """
            
            all_photos = Photo_album(search.photos_dict[hotel_id])
            """
            Создаем экземпляр класса Photo_album, который превращает обычный список в итерируемый в обе стороны.
            Используя понятные методы next и prev мы можем вращать список на 1 единицу, получая тем самым доступ к
            текущему, следующему и предыдущему объекту в списке. И используя команду send_photo отправляем первую
            имеющуюся в списке фотографию в чат бота
            """
            a = bot.send_photo(chat_id=message.chat.id, photo=str(all_photos), reply_markup=IKM_photos_sliding())
            data_add(sql_base='user_database.db', user_id=message.chat.id,
                     message_id=a.message_id, msg_content='hotel_photo_message')
            
            """
            Сохраняем в переменную отправленное сообщение, чтобы иметь возможность созданный ранее список с новыми
            функциями присвоить в словаре ключу содержащий ID сообщения. Это позволит нам идентифицировать каждое
            нажатие пользователя. У клавиатуры и сообщения, под которым появляется клавиатура, идентификаторы сообщения
            одинаковые, а значит это позволяет нам менять именно то фото, под которым была нажата кнопка, так как
            call.message.id (в следующем обработчике) и a.message.id одинаковые.
            """
            search.photos_dict_urls.update({a.message_id: all_photos})
            logging.info(lang_dict[search.lang]['command_logging']['log28'], extra=search.user_id)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'photo')
def photo_slide(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_photos_sliding
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей направление
    прокрутки фотоальбома.
    :type call: telebot.types.CallbackQuery
    :return: При нажатии на кнопку меняется фотография.
    :rtype: None
    """
    logging.info(lang_dict[search.lang]['command_logging']['log29'], extra=search.user_id)
    
    if call.data == 'next':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        
        next_photo = search.photos_dict_urls[call.message.id].next()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=next_photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding())
    
    if call.data == 'previous':
        logging.info(lang_dict[search.lang]['command_logging']['log16'].format(button=button_text(call)),
                     extra=search.user_id)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        
        prev_photo = search.photos_dict_urls[call.message.id].prev()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=prev_photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding())

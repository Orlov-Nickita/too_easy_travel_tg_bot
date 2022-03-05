import telebot
import telegram
import re
import emoji
from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot, User_search
from utils.errors import Negative_value, Max_more_min
from utils.logger import logger
from utils.sqlite_history import history_data_add
from useful_add_func.requests_rapidapiHotels import city_search, hotels_search_price, photos_for_hotel
from commands_and_keyboards.keyboards import IKM_for_hotels_poisk, IKM_for_photos_search, \
    IKM_for_city_choice, IKM_photos_sliding, IKM_date_chk_in_change, IKM_date_chk_out_change, IKM_price_distance_approve
from useful_add_func.photo_album_class import Photo_album
from useful_add_func.auxiliary_functions import date_change, yandex_maps, user_rating_false, streetaddress_false, \
    info_check, summary_check, button_text
from datetime import date
from dateutil.relativedelta import relativedelta
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    """
    Функция, предназначенная для ввода желаемого города
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :return: После ввода города Пользователем значение передается в функцию city_poisk для поиска совпадений по
    введенному наименованию города.
    :rtype: None
    """
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log6'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    first_msg = bot.send_message(chat_id=message.chat.id,
                                 text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                     'text2'])
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
        msg=first_msg.text),
        user_id=message.chat.id)
    
    bot.register_next_step_handler(message=first_msg, callback=city_poisk)


def city_poisk(message: telebot.types.Message) -> None:
    """
    Функция для нахождения совпадений по введенному наименованию города.
    :param message: В качестве параметра передается сообщение из чата с Пользователем.
    :type message: telebot.types.Message
    :return: Выводится клавиатура, содержащая наименования найденных городов близких по написанию (названию)
    к введенному, при нажатии на кнопки которой можно будет уточнить место поиска отелей.
    :rtype: None
    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log8'],
                user_id=message.chat.id)
    
    User_search().get_user(user_id=message.chat.id).found_cities = dict()
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    User_search().get_user(user_id=message.chat.id).city = message.text.title()
    
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text3'].format(city=User_search().get_user(user_id=message.chat.id).city))
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log3'].format(
        msg=msg.text),
        user_id=message.chat.id)
    
    for group in city_search(
            message=msg,
            locale=User_search().get_user(user_id=message.chat.id).locale,
            city_name=User_search().get_user(user_id=message.chat.id).city,
            currency=User_search().get_user(user_id=message.chat.id).currency
    )['suggestions']:
        if group['group'] == 'CITY_GROUP':
            for something in group['entities']:
                User_search().get_user(user_id=message.chat.id).found_cities.update(
                    {re.sub(r"<span class='highlighted'>|</span>", '',
                            something['caption']): int(something['destinationId'])})
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    
    msg2 = bot.send_message(chat_id=message.chat.id,
                            text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                'text4'].format(city=User_search().get_user(user_id=message.chat.id).city),
                            reply_markup=IKM_for_city_choice(
                                User_search().get_user(user_id=message.chat.id).found_cities)
                            )
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log9'].format(
        msg2=msg2.text, cities=User_search().get_user(user_id=message.chat.id).found_cities),
        user_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text4.1']))
def city_choice_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_city_choice
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши, содержащей название города
    :type call: telebot.types.CallbackQuery
    :return: Значение нажатой кнопки передается в функцию qty_hotels для определения желаемого количество отелей
    для поиска
    :rtype: None
    """
    User_search().get_user(user_id=call.message.chat.id).city_id = call.data
    temp_call = call
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.edit_message_text(
        text=lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text28'].format(
            city=User_search().get_user(user_id=call.message.chat.id).city,
            button=button_text(call)),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode=telegram.ParseMode.HTML)
    
    logger.info(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log10'].format(
            button=button_text(temp_call)),
        user_id=call.message.chat.id)
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log11'],
                user_id=call.message.chat.id)
    
    bot.answer_callback_query(callback_query_id=temp_call.id,
                              text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                    ).lang]['command_acq']['acq2'])
    bot.send_chat_action(chat_id=temp_call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    check_in_date_choice(temp_call.message)


def check_in_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты въезда в отель через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log12'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    calendar, step = DetailedTelegramCalendar(calendar_id=1,
                                              locale=User_search().get_user(user_id=message.chat.id).lang,
                                              min_date=date.today(),
                                              max_date=date.today() + relativedelta(months=2)).build()
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text5'],
                           reply_markup=calendar)
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log3'].format(
        msg=msg.text),
        user_id=message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def chk_in_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logger.info(lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command_logging']['log13'],
                user_id=c.message.chat.id)
    
    result, key, step = DetailedTelegramCalendar(calendar_id=1,
                                                 locale=User_search().get_user(user_id=c.message.chat.id).lang,
                                                 min_date=date.today(),
                                                 max_date=date.today() + relativedelta(months=2)).process(c.data)
    if not result and key:
        bot.edit_message_text(
            text=lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command']['text5'],
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=key)
    elif result:
        User_search().get_user(user_id=c.message.chat.id).check_in = result
        bot.edit_message_text(
            text=lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command']['text6'].format(
                res=date_change(result)),
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=IKM_date_chk_in_change(c.message)
        )
        logger.info(
            lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command_logging']['log14'].format(
                time_res=User_search().get_user(user_id=c.message.chat.id).check_in),
            username=c.message.from_user.username,
            user_id=c.message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text6.1']))
def chk_in_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    temp_call = call
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log15'],
                user_id=call.message.chat.id)
    
    if temp_call.data == 'cancel':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.delete_message(chat_id=temp_call.message.chat.id, message_id=temp_call.message.message_id)
        check_in_date_choice(temp_call.message)
    
    elif temp_call.data == 'continue':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        check_out_date_choice(temp_call.message)


def check_out_date_choice(message: telebot.types.Message) -> None:
    """
    Функция для инициализации процесса выбора даты выезда из отеля через календарь
    :param message: В качестве параметра передается сообщение
    :type message: telebot.types.Message
    :return: Создается календарь для выбора даты въезда
    :rtype None
    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log17'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    calendar, step = DetailedTelegramCalendar(calendar_id=2,
                                              locale=User_search().get_user(user_id=message.chat.id).lang,
                                              min_date=User_search().get_user(
                                                  user_id=message.chat.id).check_in + relativedelta(days=1),
                                              max_date=User_search().get_user(
                                                  user_id=message.chat.id).check_in + relativedelta(
                                                  months=2)).build()
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text7'],
                           reply_markup=calendar)
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log3'].format(
        msg=msg.text),
        user_id=message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def chk_out_date_calendar(c: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки календаря
    :param c: Параметр содержит callback_data нажатой кнопки, сначала год, затем месяц
    :type c: telebot.types.CallbackQuery
    :return: Результатом выполнения является выбранная дата въезда Пользователя
    :rtype: None
    """
    logger.info(lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command_logging']['log18'],
                user_id=c.message.chat.id)
    
    result, key, step = DetailedTelegramCalendar(calendar_id=2,
                                                 locale=User_search().get_user(user_id=c.message.chat.id).lang,
                                                 min_date=User_search().get_user(
                                                     user_id=c.message.chat.id).check_in + relativedelta(days=1),
                                                 max_date=User_search().get_user(
                                                     user_id=c.message.chat.id).check_in + relativedelta(
                                                     months=2)).process(c.data)
    if not result and key:
        bot.edit_message_text(
            text=lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command']['text7'],
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=key)
    elif result:
        if result == User_search().get_user(user_id=c.message.chat.id).check_in:
            bot.answer_callback_query(callback_query_id=c.id,
                                      text=lang_dict[User_search().get_user(user_id=c.message.chat.id
                                                                            ).lang]['command']['text9'],
                                      show_alert=True)
            logger.info(
                lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command_logging'][
                    'log19'].format(
                    time_res=date_change(result)),
                user_id=c.message.chat.id)
            bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
            
            check_out_date_choice(c.message)
        else:
            User_search().get_user(user_id=c.message.chat.id).check_out = result
            bot.edit_message_text(
                text=lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command']['text8'].format(
                    res=date_change(result)),
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                reply_markup=IKM_date_chk_out_change(c.message))
            logger.info(
                lang_dict[User_search().get_user(user_id=c.message.chat.id).lang]['command_logging'][
                    'log20'].format(
                    time_res=User_search().get_user(user_id=c.message.chat.id).check_out),
                user_id=c.message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text8.1']))
def chk_out_date_change(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение даты, либо переход к
    следующему шагу - выбору даты выезда
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    temp_call = call
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log21'],
                user_id=call.message.chat.id)
    
    if temp_call.data == 'cancel':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.delete_message(chat_id=temp_call.message.chat.id, message_id=temp_call.message.message_id)
        check_out_date_choice(temp_call.message)
    
    elif temp_call.data == 'continue':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        
        if User_search().get_user(user_id=call.message.chat.id).sort == 'DISTANCE_FROM_LANDMARK':
            price_range(temp_call.message)
        else:
            qty_hotels(temp_call.message)


def price_range(message: telebot.types.Message) -> None:
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log30'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text13'])
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
        msg=msg.text),
        user_id=message.chat.id)
    
    bot.register_next_step_handler(message=msg, callback=price_limiter)


def price_limiter(message: telebot.types.Message) -> None:
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log41'].format(
        msg=message.text),
        user_id=message.chat.id)
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log31'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    try:
        User_search().get_user(user_id=message.chat.id).min_price, User_search().get_user(
            user_id=message.chat.id).max_price = int(message.text.split()[0]), int(message.text.split()[1])
        
        if User_search().get_user(user_id=message.chat.id).max_price <= User_search().get_user(
                user_id=message.chat.id).min_price:
            raise Max_more_min
        
        elif User_search().get_user(user_id=message.chat.id).min_price < 0 or User_search().get_user(
                user_id=message.chat.id).max_price < 0:
            raise Negative_value
    
    except IndexError as Ex:
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log37'],
                    user_id=message.chat.id)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text18'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log38'].format(Ex),
            user_id=message.chat.id)
        price_range(message=message)
    
    except Negative_value:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text20'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        price_range(message=message)
    
    except Max_more_min:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text21'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        price_range(message=message)
    
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text22'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        price_range(message=message)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text15'].format(User_search().get_user(user_id=message.chat.id).min_price,
                                                    User_search().get_user(user_id=message.chat.id).max_price),
                               reply_markup=IKM_price_distance_approve(message))
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text15.1']))
def price_limiter_approve(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение расстояния, либо переход к
    следующему шагу - количество отелей
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log34'],
                user_id=call.message.chat.id)
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    if call.data == 'cancel':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        price_range(call.message)
    
    elif call.data == 'continue':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        distance_range(call.message)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def distance_range(message: telebot.types.Message) -> None:
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log32'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text14'])
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
        msg=msg.text),
        user_id=message.chat.id)
    
    bot.register_next_step_handler(message=msg, callback=distance_limiter)


def distance_limiter(message: telebot.types.Message) -> None:
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log41'].format(
        msg=message.text),
        user_id=message.chat.id)
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log33'],
                user_id=message.chat.id)
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    try:
        User_search().get_user(user_id=message.chat.id).min_dist, User_search().get_user(
            user_id=message.chat.id).max_dist = int(message.text.split()[0]), int(message.text.split()[1])
    
    except IndexError as Ex:
        
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log39'],
                    user_id=message.chat.id)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text19'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log40'].format(Ex),
            user_id=message.chat.id)
        distance_range(message=message)
    
    except Negative_value:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text23'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        distance_range(message=message)
    
    except Max_more_min:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text24'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        distance_range(message=message)
    
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text22'])
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)
        distance_range(message=message)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                   'text16'].format(User_search().get_user(user_id=message.chat.id).min_dist,
                                                    User_search().get_user(user_id=message.chat.id).max_dist),
                               reply_markup=IKM_price_distance_approve(message))
        logger.info(
            lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log7'].format(
                msg=msg.text),
            user_id=message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text16.1'].format(
            User_search().get_user(user_id=call.message.chat.id).min_dist,
            User_search().get_user(user_id=call.message.chat.id).max_dist)))
def distance_limiter_approve(call: telebot.types.CallbackQuery) -> None:
    """
    Функция-обработчик нажатия кнопок на клавиатуре
    :param call: Параметр содержит в себе команду выбранную Пользователем. Либо изменение цен, либо переход к
    следующему шагу - выбору диапозона расстояния
    :type call:telebot.types.CallbackQuery
    :return: Либо выбор даты въезда начинается снова, либо переход к следующему шагу по выбору даты выезда
    :rtype: None
    """
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log35'],
                user_id=call.message.chat.id)
    bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    if call.data == 'cancel':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        distance_range(call.message)
    
    elif call.data == 'continue':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
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
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log22'],
                user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                               'text10'],
                           reply_markup=IKM_for_hotels_poisk()
                           )
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log3'].format(
        msg=msg.text),
        user_id=message.chat.id)
    
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text10']))
def city_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_hotels_poisk
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей количество отелей
    :type call: call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_poisk_in_the_city
    :rtype: None
    """
    User_search().get_user(user_id=call.message.chat.id).hotels_qty = int(call.data)
    
    temp_call = call
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.edit_message_text(
        text=lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text25'].format(
            button=button_text(call)),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode=telegram.ParseMode.HTML)
    
    bot.send_chat_action(chat_id=temp_call.message.chat.id, action=telegram.ChatAction.TYPING)
    bot.answer_callback_query(callback_query_id=temp_call.id,
                              text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                    ).lang]['command_acq']['acq2'])
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log23'],
                user_id=call.message.chat.id)
    
    logger.info(
        lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log16'].format(
            button=button_text(temp_call)),
        username=call.message.from_user.username,
        user_id=call.message.chat.id)
    bot.send_chat_action(chat_id=temp_call.message.chat.id, action=telegram.ChatAction.TYPING)
    hotels_poisk_in_the_city(message=temp_call.message,
                             hotels_qty=User_search().get_user(user_id=call.message.chat.id).hotels_qty)


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
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log24'],
                user_id=message.chat.id)
    
    User_search().get_user(user_id=message.chat.id).hotels = dict()
    count = 0
    bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
    
    while True:
        for hotel in \
                hotels_search_price(message=message,
                                    city_destination_id=User_search().get_user(user_id=message.chat.id).city_id,
                                    pagenumber=User_search().get_user(user_id=message.chat.id).pagenumber,
                                    chk_in=User_search().get_user(user_id=message.chat.id).check_in,
                                    chk_out=User_search().get_user(user_id=message.chat.id).check_out,
                                    min_price=User_search().get_user(user_id=message.chat.id).min_price,
                                    max_price=User_search().get_user(user_id=message.chat.id).max_price,
                                    sort=User_search().get_user(user_id=message.chat.id).sort,
                                    locale=User_search().get_user(user_id=message.chat.id).locale,
                                    currency=User_search().get_user(user_id=message.chat.id).currency
                                    )['data']['body']['searchResults']['results']:
            
            bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
            logger.info(
                lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log36'].format(
                    User_search().get_user(user_id=message.chat.id).pagenumber),
                user_id=message.chat.id)
            landmark_distance = float(hotel['landmarks'][0]['distance'].split()[0].replace(',', '.')) * 1000
            
            if User_search().get_user(user_id=message.chat.id).sort == 'DISTANCE_FROM_LANDMARK' and (
                    landmark_distance >= User_search().get_user(user_id=message.chat.id).max_dist or
                    landmark_distance <= User_search().get_user(user_id=message.chat.id).min_dist):
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                continue
            
            else:
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                User_search().get_user(user_id=message.chat.id).hotels.update({hotel['name']: {
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key1']: hotel['id'],
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key2']: '{}, {}'.format(
                        hotel['address']['locality'],
                        streetaddress_false(hotel)),
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key3']: hotel['coordinate'],
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key4']: hotel['landmarks'][0]['distance'],
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key5']: '{price} {days} {tax}'.format(
                        price=hotel['ratePlan']['price']['current'],
                        days=info_check(hotel),
                        tax=summary_check(hotel)
                    ),
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key6']: int(
                        hotel['ratePlan']['price']['exactCurrent'] / int(
                            str(User_search().get_user(user_id=message.chat.id).check_out - User_search().get_user(
                                user_id=message.chat.id).check_in).split()[0])
                    ),
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key7']: '{stars} звезд{letter}'.format(
                        stars=hotel['starRating'],
                        letter='а' if hotel['starRating'] == 1
                        else 'ы'
                    ),
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                        'key8']: '{user_rating}'.format(
                        user_rating=user_rating_false(hotel)),
                    lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
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
                                   text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command'][
                                       'text11'],
                                   reply_markup=IKM_for_photos_search(message)
                                   )
            logger.info(
                lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log3'].format(
                    msg=msg.text),
                user_id=message.chat.id)
            break
        else:
            User_search().get_user(user_id=message.chat.id).pagenumber += 1
            
            if User_search().get_user(user_id=message.chat.id).pagenumber == 4:
                bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
                msg = bot.send_message(chat_id=message.chat.id,
                                       text=lang_dict[User_search().get_user(user_id=message.chat.id
                                                                             ).lang]['command']['text17'])
                logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging'][
                                'log3'].format(msg=msg.text),
                            user_id=message.chat.id)
                User_search().get_user(user_id=message.chat.id).pagenumber = 1
                
                check_in_date_choice(message=message)
                
                break


@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.startswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text11']))
def hotels_poisk_keyboard_callback(call: telebot.types.CallbackQuery) -> None:
    """
    Функция предназначенная для обработки нажатия на кнопки IKM_for_photos_search
    :param call: В качестве параметра передается значение callback_data нажатой кнопки, содержащей ответ о
    необходимости фотографий
    :type call: telebot.types.CallbackQuery
    :return: Значение передается в функцию hotels_info
    :rtype: None
    """
    temp_call = call
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.edit_message_text(
        text=lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command']['text26'].format(
            button=button_text(call)),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode=telegram.ParseMode.HTML)
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log25'],
                user_id=call.message.chat.id)
    
    bot.send_chat_action(chat_id=temp_call.message.chat.id, action=telegram.ChatAction.TYPING)
    
    bot.answer_callback_query(callback_query_id=temp_call.id,
                              text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                    ).lang]['command_acq']['acq3'])
    
    if temp_call.data == 'Yes':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        hotels_info(temp_call.message, User_search().get_user(user_id=call.message.chat.id).hotels,
                    photo_need=True)
    
    if temp_call.data == 'No':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(temp_call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        hotels_info(temp_call.message, User_search().get_user(user_id=call.message.chat.id).hotels,
                    photo_need=False)


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
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log26'],
                user_id=message.chat.id)
    User_search().get_user(user_id=message.chat.id).photos_dict = dict()
    User_search().get_user(user_id=message.chat.id).photos_dict_urls = dict()
    for every_hotel in found_hotels:
        bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.TYPING)
        msg_info = bot.send_message(chat_id=message.chat.id,
                                    text=lang_dict[User_search().get_user(user_id=message.chat.id
                                                                          ).lang]['command']['text12'].format(
                                        emoji1=emoji.emojize(":hotel:", use_aliases=True),
                                        hotel_name=every_hotel,
                                        emoji2=emoji.emojize(":globe_with_meridians:", use_aliases=True),
                                        web=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key9']],
                                        emoji3=emoji.emojize(":earth_americas:", use_aliases=True),
                                        address=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key2']],
                                        emoji4=emoji.emojize(":pushpin:", use_aliases=True),
                                        yamaps=yandex_maps(found_hotels[every_hotel][
                                                               lang_dict[User_search().get_user(
                                                                   user_id=message.chat.id).lang][
                                                                   'command_print_search_info'][
                                                                   'key3']][
                                                               'lat'],
                                                           found_hotels[every_hotel][
                                                               lang_dict[User_search().get_user(
                                                                   user_id=message.chat.id).lang][
                                                                   'command_print_search_info'][
                                                                   'key3']]['lon']
                                                           ),
                                        emoji5=emoji.emojize(":left_right_arrow:", use_aliases=True),
                                        center=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key4']],
                                        emoji6=emoji.emojize(":credit_card:", use_aliases=True),
                                        price=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key5']],
                                        emoji7=emoji.emojize(":soon:", use_aliases=True),
                                        emoji8=emoji.emojize(":back:", use_aliases=True),
                                        chk_in_date=date_change(
                                            User_search().get_user(user_id=message.chat.id).check_in),
                                        chk_out_date=date_change(
                                            User_search().get_user(user_id=message.chat.id).check_out),
                                        emoji9=emoji.emojize(":one:", use_aliases=True),
                                        one_day_price='{0:,} {cur}'.format(
                                            found_hotels[every_hotel][
                                                lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                    'command_print_search_info']['key6']],
                                            cur=User_search().get_user(user_id=message.chat.id).currency),
                                        emoji10=emoji.emojize(":star:", use_aliases=True),
                                        rating=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key7']],
                                        emoji11=emoji.emojize(":sparkles:", use_aliases=True),
                                        user_rating=found_hotels[every_hotel][
                                            lang_dict[User_search().get_user(user_id=message.chat.id).lang][
                                                'command_print_search_info']['key8']],
                                    ),
                                    parse_mode=telegram.ParseMode.HTML,
                                    disable_web_page_preview=True
                                    )
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log27'],
                    user_id=message.chat.id)
        history_data_add(sql_base='user_database.db', user_id=message.chat.id,
                         message_id=msg_info.message_id, msg_content='hotel_information_message')
        
        if photo_need:
            bot.send_chat_action(chat_id=message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
            
            hotel_id = found_hotels[every_hotel][
                lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_print_search_info'][
                    'key1']]
            """
            В рамках общего цикла, где мы перебираем все отели от 1 до выбранного количества Пользователем, мы сохраняем
            значение ID каждого из этих отелей в переменную
            """
            hotel_photos = photos_for_hotel(message=message, hotel_id=hotel_id)
            """
            Получив ранее ID отеля, мы обращаемся к функции photos_for_hotel для того чтобы получить JSON ответ,
            содержащий фотографии отеля
            """
            User_search().get_user(user_id=message.chat.id).photos_dict[hotel_id] = list()
            """
            В экземпляре класса User_search в атрибуте photos_dict создается пустой список, в который далее мы
            сохраним все имеющиеся фотографии в виде ссылок
            """
            for every_photos in hotel_photos['hotelImages']:
                """
                Циклом проходим по всем имеющимся фотографиям в JSON ответе с сервера
                """
                User_search().get_user(user_id=message.chat.id).photos_dict[hotel_id].append(
                    every_photos['baseUrl'].format(size=every_photos['sizes'][0]['suffix']))
                """
                А теперь в атрибут photos_dict, где создан пустой список, добавляем все ссылки циклом, так как они все
                лежат в определенных местах независимо друг от друга
                """
            
            all_photos = Photo_album(User_search().get_user(user_id=message.chat.id).photos_dict[hotel_id])
            """
            Создаем экземпляр класса Photo_album, который превращает обычный список в итерируемый в обе стороны.
            Используя понятные методы next и prev мы можем вращать список на 1 единицу, получая тем самым доступ к
            текущему, следующему и предыдущему объекту в списке. И используя команду send_photo отправляем первую
            имеющуюся в списке фотографию в чат бота
            """
            a = bot.send_photo(chat_id=message.chat.id, photo=str(all_photos), reply_markup=IKM_photos_sliding(message))
            history_data_add(sql_base='user_database.db', user_id=message.chat.id,
                             message_id=a.message_id, msg_content='hotel_photo_message')
            
            """
            Сохраняем в переменную отправленное сообщение, чтобы иметь возможность созданный ранее список с новыми
            функциями присвоить в словаре ключу содержащий ID сообщения. Это позволит нам идентифицировать каждое
            нажатие пользователя. У клавиатуры и сообщения, под которым появляется клавиатура, идентификаторы сообщения
            одинаковые, а значит это позволяет нам менять именно то фото, под которым была нажата кнопка, так как
            call.message.id (в следующем обработчике) и a.message.id одинаковые.
            """
            User_search().get_user(user_id=message.chat.id).photos_dict_urls.update({a.message_id: all_photos})
            logger.info(
                lang_dict[User_search().get_user(user_id=message.chat.id).lang]['command_logging']['log28'],
                user_id=message.chat.id)


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
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging']['log29'],
                user_id=call.message.chat.id)
    
    if call.data == 'next':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        
        next_photo = User_search().get_user(user_id=call.message.chat.id).photos_dict_urls[call.message.id].next()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=next_photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding(call.message))
    
    if call.data == 'previous':
        logger.info(
            lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['command_logging'][
                'log16'].format(
                button=button_text(call)),
            username=call.message.from_user.username,
            user_id=call.message.chat.id)
        bot.send_chat_action(chat_id=call.message.chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        
        prev_photo = User_search().get_user(user_id=call.message.chat.id).photos_dict_urls[call.message.id].prev()
        bot.edit_message_media(media=telebot.types.InputMedia(type='photo',
                                                              media=prev_photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id,
                               reply_markup=IKM_photos_sliding(call.message))

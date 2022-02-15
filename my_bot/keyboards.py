import emoji
import telegram
from telebot import types
from location_by_ip_address import ip_search
from typing import Dict

from utils.languages_for_bot import lang_dict
from loader import search


def IKM_for_greeting_msg() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру при запуске команды поиска отелей. Функция ip_search() определяет
    местоположение Пользователя и предлагает сделать поиск отеля по этому местоположению или задать другой город для
    поиска
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_greeting_msg = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(
        text=lang_dict[search.lang]['keyboards']['IKM_for_greeting_msg']['text1'].format(ip_search()),
        callback_data=ip_search())
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_greeting_msg']['text2'],
                                       callback_data='No')
    
    ikm_greeting_msg.add(item1, item2)
    
    return ikm_greeting_msg


def IKM_for_city_choice(found_cities_dict: Dict) -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру со всеми найденными местоположениями
    :param found_cities_dict: В качестве параметра передается словарь из найденных местоположений по введенному запросу.
    В качестве ключа в словаре содержится название города, в качестве значения ключа id города с rapidapi для
    последующего поиска отелей в выбранном месте
    :type found_cities_dict: Dict
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_cities_found = types.InlineKeyboardMarkup()
    
    for i_city in found_cities_dict:
        ikm_cities_found.add(
            types.InlineKeyboardButton(text=i_city, callback_data=found_cities_dict[i_city]))
    ikm_cities_found.add(
        types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_city_choice']['text1'],
                                   callback_data='Back'))
    
    return ikm_cities_found


def IKM_for_hotels_poisk() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для выбора необходимого Пользователю количества отелей
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_hotels_qty = types.InlineKeyboardMarkup(row_width=4)
    
    item1 = types.InlineKeyboardButton(text='1', callback_data=1)
    item2 = types.InlineKeyboardButton(text='2', callback_data=2)
    item3 = types.InlineKeyboardButton(text='3', callback_data=3)
    item4 = types.InlineKeyboardButton(text='4', callback_data=4)
    item5 = types.InlineKeyboardButton(text='5', callback_data=5)
    item6 = types.InlineKeyboardButton(text='10', callback_data=10)
    item7 = types.InlineKeyboardButton(text='15', callback_data=15)
    item8 = types.InlineKeyboardButton(text='20', callback_data=20)
    item9 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_hotels_poisk']['text1'],
                                       callback_data='Back')
    
    ikm_hotels_qty.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    
    return ikm_hotels_qty


def IKM_for_photos_search() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для принятия решения о необходимости фотографий для ознакомления с отелем
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_hotels_photo = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_photos_search']['text1'],
                                       callback_data='Yes')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_photos_search']['text2'],
                                       callback_data='No')
    
    item3 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_photos_search']['text3'],
                                       callback_data='Back')
    
    ikm_hotels_photo.add(item1, item2, item3)
    
    return ikm_hotels_photo


def IKM_photos_sliding() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для смены фотографий в фотоальбоме для отелей
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_photo_slide = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_photos_sliding']['text1'],
                                       callback_data='previous')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_photos_sliding']['text2'],
                                       callback_data='next')
    
    ikm_photo_slide.add(item1, item2)
    
    return ikm_photo_slide


def IKM_date_chk_in_change() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для подтверждения даты въезда
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_chk_in_date_change = types.InlineKeyboardMarkup()
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_date_chk_in_change']['text1'],
                                       callback_data='cancel')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_date_chk_in_change']['text2'],
                                       callback_data='continue')
    ikm_chk_in_date_change.add(item1, item2)
    
    return ikm_chk_in_date_change


def IKM_date_chk_out_change() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для подтверждения даты выезда
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_chk_out_date_change = types.InlineKeyboardMarkup()
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_date_chk_out_change']['text1'],
                                       callback_data='cancel')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_date_chk_out_change']['text2'],
                                       callback_data='continue')
    ikm_chk_out_date_change.add(item1, item2)
    
    return ikm_chk_out_date_change


def IKM_for_settings() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру с командами выбора языка или валюты
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_for_settings = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_settings']['text1'],
                                       callback_data='language')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_for_settings']['text2'],
                                       callback_data='currency')
    
    ikm_for_settings.add(item1, item2)
    
    return ikm_for_settings


def IKM_settings_lang() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру с командой выбора языка
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_settings_lang = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_settings_lang']['text1'],
                                       callback_data='ru')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_settings_lang']['text2'],
                                       callback_data='en')
    
    item3 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_settings_lang']['text3'],
                                       callback_data='mainmenu')
    
    ikm_settings_lang.add(item1, item2, item3)
    
    return ikm_settings_lang


def IKM_settings_currency() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру с командой выбора валюты
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_settings_currency = types.InlineKeyboardMarkup()
    
    item1 = types.InlineKeyboardButton(
        text=lang_dict[search.lang]['keyboards']['IKM_settings_currency']['text1'].format(
            emoji1=emoji.emojize(":pound:", use_aliases=True)),
        callback_data='RUB')

    item2 = types.InlineKeyboardButton(
        text=lang_dict[search.lang]['keyboards']['IKM_settings_currency']['text2'].format(
            emoji2=emoji.emojize(":dollar:", use_aliases=True)),
        callback_data='USD')
    
    item3 = types.InlineKeyboardButton(
        text=lang_dict[search.lang]['keyboards']['IKM_settings_currency']['text3'].format(
            emoji3=emoji.emojize(":euro:", use_aliases=True)),
        callback_data='EUR')
    
    item4 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_settings_currency']['text4'],
                                       callback_data='mainmenu')
    
    ikm_settings_currency.add(item1, item2, item3, item4)
    
    return ikm_settings_currency


def IKM_price_distance_approve() -> types.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для подтверждения диапазонов цен и расстояния от центра для отелей
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_price_distance_approve = types.InlineKeyboardMarkup()
    
    item1 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_price_distance_approve']['text1'],
                                       callback_data='cancel')
    
    item2 = types.InlineKeyboardButton(text=lang_dict[search.lang]['keyboards']['IKM_price_distance_approve']['text2'],
                                       callback_data='continue')
    ikm_price_distance_approve.add(item1, item2)
    
    return ikm_price_distance_approve
import telegram
from telebot import types
from location_by_ip_address import ip_search
from typing import Dict


def IKM_for_greeting_msg() -> telegram.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру при запуске команды поиска отелей. Функция ip_search() определяет
    местоположение Пользователя и предлагает сделать поиск отеля по этому местоположению или задать другой город для
    поиска
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_greeting_msg = types.InlineKeyboardMarkup(row_width = 2)
    
    item1 = types.InlineKeyboardButton(text = f'{ip_search()}', callback_data = ip_search())
    item2 = types.InlineKeyboardButton(text = 'Выбрать другой город', callback_data = 'No')
    
    ikm_greeting_msg.add(item1, item2)
    
    return ikm_greeting_msg


def IKM_for_city_choice(found_cities_dict: Dict) -> telegram.InlineKeyboardMarkup:
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
        ikm_cities_found.add(types.InlineKeyboardButton(text = i_city, callback_data = found_cities_dict[i_city]))
    ikm_cities_found.add(types.InlineKeyboardButton(text = 'Вернуться назад', callback_data = 'Back'))
    
    return ikm_cities_found


def IKM_for_hotels_poisk() -> telegram.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для выбора необходимого Пользователю количества отелей
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
    """
    ikm_hotels_qty = types.InlineKeyboardMarkup(row_width = 4)
    
    item1 = types.InlineKeyboardButton(text = '1', callback_data = 1)
    item2 = types.InlineKeyboardButton(text = '2', callback_data = 2)
    item3 = types.InlineKeyboardButton(text = '3', callback_data = 3)
    item4 = types.InlineKeyboardButton(text = '4', callback_data = 4)
    item5 = types.InlineKeyboardButton(text = '5', callback_data = 5)
    item6 = types.InlineKeyboardButton(text = '10', callback_data = 10)
    item7 = types.InlineKeyboardButton(text = '15', callback_data = 15)
    item8 = types.InlineKeyboardButton(text = '20', callback_data = 20)
    item9 = types.InlineKeyboardButton(text = 'Вернуться назад', callback_data = 'Back')
    
    ikm_hotels_qty.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    
    return ikm_hotels_qty


def IKM_for_photos_search() -> telegram.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для принятия решения о необходимости фотографий для ознакомления с отелем
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup

    """
    ikm_hotels_photo = types.InlineKeyboardMarkup(row_width = 2)
    
    item1 = types.InlineKeyboardButton(text = 'Да', callback_data = 'Да')
    item2 = types.InlineKeyboardButton(text = 'Нет', callback_data = 'Нет')
    item3 = types.InlineKeyboardButton(text = 'Вернуться назад', callback_data = 'Back')
    
    ikm_hotels_photo.add(item1, item2, item3)
    
    return ikm_hotels_photo


def IKM_photos_sliding() -> telegram.InlineKeyboardMarkup:
    """
    Функция, которая определяет клавиатуру для смены фотографий в фотоальбоме для отелей
    :return: Возвращается клавиатура (функция) как объект
    :rtype: telegram.InlineKeyboardMarkup
 
    """
    ikm_photo_slide = types.InlineKeyboardMarkup(row_width = 2)
    
    item1 = types.InlineKeyboardButton(text = '< Листать фото', callback_data = 'previous')
    item2 = types.InlineKeyboardButton(text = 'Листать фото >', callback_data = 'next')
    
    ikm_photo_slide.add(item1, item2)
    
    return ikm_photo_slide
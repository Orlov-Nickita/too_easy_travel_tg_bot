from typing import List

import telebot
import re
from datetime import datetime


def date_change(some_date: datetime.date) -> str:
    """
    Функция для изменения формата даты после выбора даты в календаре
    :param some_date: Строка в виде даты ГОД-МЕСЯЦ-ДЕНЬ (YYYY-MM-DD), которая образуется после выбора даты в календаре
    :type some_date: str
    :return: Возвращается отформатированная строка с датой
    """
    chk_in_date = datetime.strftime(some_date, "%d.%m.%Y")
    return chk_in_date


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


def button_text(button_call: telebot.types.CallbackQuery):
    """
    Функция для определения нажатой кнопки Пользователем
    :param button_call: Параметр содержит callback_data нажатой кнопки
    :type button_call:  telebot.types.CallbackQuery
    :return: Возвращается текст, который написан на кнопке, чтобы определить, на какую именно кнопку нажал пользователь
    """
    
    def keyboard_buttons_unpack(inline_key: List) -> List:
        """
        Функция-рекурсия для создания одноуровневого списка из многоуровневого списка
        :param inline_key: Параметр содержит многоуровневый список всех кнопок в клавиатуре, которая содержится в
        параметре Call нажатой кнопки
        :type inline_key: List
        :return: Возвращается одноуровневый список словарей со всеми кнопками
        """
        new_list = list()
        for i in inline_key:
            if isinstance(i, list):
                new_list.extend(keyboard_buttons_unpack(i))
            else:
                new_list.append(i)
        return new_list
    
    def text_button_pressed(but_list: List, call: telebot.types.CallbackQuery) -> str:
        """
        Функция для нахождения нажатой кнопки
        :param but_list: Параметр содержит список словарей с кнопками
        :type but_list: List
        :param call: Параметр содержит словарь данных нажатой кнопки
        :type call: telebot.types.CallbackQuery
        :return: Возвращается текст нажатой кнопки
        """
        for i in but_list:
            if i['callback_data'] == call.data:
                return i['text']
    
    a = keyboard_buttons_unpack(button_call.message.json['reply_markup']['inline_keyboard'])
    return text_button_pressed(a, button_call)


def user_rating_false(hotel):  # Я пока не решил проблему отсутствия в некоторых местах тех или иных параметров.
    # Наверно для этих случаев надо мне сделать одну общую функцию, которая будет делать проверку ключей в словаре.
    # Пока так оставил эту и следующую
    try:
        return hotel['guestReviews']
    except KeyError:
        return ''


def streetaddress_false(hotel):  # Я пока не решил проблему отсутствия в некоторых местах тех или иных параметров.
    # Наверно для этих случаев надо мне сделать одну общую функцию, которая будет делать проверку ключей в словаре.
    # Пока так оставил эту и следующую
    try:
        return hotel['address']['streetAddress']
    except KeyError:
        return ''


def info_check(info):  # Я пока не решил проблему отсутствия в некоторых местах тех или иных параметров.
    # Наверно для этих случаев надо мне сделать одну общую функцию, которая будет делать проверку ключей в словаре.
    # Пока так оставил эту и следующую
    try:
        return info['ratePlan']['price']['info']
    except KeyError:
        return ''


def summary_check(info):  # Я пока не решил проблему отсутствия в некоторых местах тех или иных параметров.
    # Наверно для этих случаев надо мне сделать одну общую функцию, которая будет делать проверку ключей в словаре.
    # Пока так оставил эту
    try:
        return info['ratePlan']['price']['summary']
    except KeyError:
        return ''


def greeting_check(greeting_message: telebot.types.Message) -> bool:  # Не знаю насколько она нужна, пока оставил
    """
    Функция, предназначенная для определения приветствия от Пользователя
    :param greeting_message: В качестве параметра передается сообщение Пользователя из бота
    :type greeting_message: telebot.types.Message
    :return: Возвращается True или False после проверки соответствия сообщения Пользователя заданному шаблону
    :rtype: bool
    """
    if re.fullmatch(r'.риве.\S?', greeting_message.text):
        return True
    else:
        return False

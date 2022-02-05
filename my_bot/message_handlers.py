import telebot.types
from my_bot import lowprice, start, text, hello_world, settings, history
from loader import bot
import logging

from languages_for_bot import lang_dict
from loader import search
from sqlite import data_add


@bot.message_handler(commands=['start'])
def send_welcome_func(message: telebot.types.Message) -> None:
    """
    Функция, которая реагирует на команду /start при запуске бота и отправляет Пользователю приветствие
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    logging.info(lang_dict[search.lang]['message_handlers_logging']['log1'])
    search.lang = message.from_user.language_code
    start.start(message)


# @bot.message_handler(commands=['hello_world'])
# def hello_world_func(message: telebot.types.Message):
#     """
#     Функция, которая реагирует на команду /hello_world и отправляет приветствие Пользователю.
#     :param message: В качестве параметра передается сообщение из чата
#     :type message: telebot.types.Message
#     :return: Отправляется сообщение в чат
#     :rtype: telebot.types.Message
#
#     """
#     logging.info(lang_dict[search.lang]['message_handlers_logging']['log2'])
#     hello_world.start(message)


@bot.message_handler(commands=['lowprice'])
def low_price_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    data_add('user_database.db', message.chat.id, message.id, message.text)
    logging.info(lang_dict[search.lang]['message_handlers_logging']['log3'])
    lowprice.start(message)

#
# @bot.message_handler(commands=['highprice'])
# def high_price_func(message: telebot.types.Message) -> None:
#     """
#     Задекорированная функция для запуска скрипта по команде /highprice и поиска самых дешевых отелей в городе
#     :param message: В качестве параметра передается сообщение с командой /highprice
#     :type message: telebot.types.Message
#     :return: None
#     :rtype: telebot.types.Message
#     """
#     data_add('user_database.db', message.chat.id, message.id, message.text)
#     logging.info(lang_dict[search.lang]['message_handlers_logging']['log4'])
#     highprice.start(message)


@bot.message_handler(commands=['history'])
def history_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    logging.info(lang_dict[search.lang]['message_handlers_logging']['log7'])
    history.start(message)


@bot.message_handler(commands=['settings'])
def settings_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /highprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /highprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    logging.info(lang_dict[search.lang]['message_handlers_logging']['log5'])
    settings.start(message)


@bot.message_handler(content_types=['text'])
def text_func(message: telebot.types.Message):
    """
    Функция, которая реагирует на приветствие пользователя чата либо отвечает что не знает такой команды.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message

    """
    logging.info(lang_dict[search.lang]['message_handlers_logging']['log6'])
    text.start(message)

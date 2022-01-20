import emoji
import telebot.types
import lowprice
from loader import bot
import logging
from Logger import log_log
from auxiliary_functions import greeting_check


@bot.message_handler(commands = ['start'])
def send_welcome(message: telebot.types.Message) -> None:
    """
    Функция, которая реагирует на команду /start при запуске бота и отправляет Пользователю приветствие
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    log_log(message)
    logging.info('Запущена команда /start')
    bot.send_message(chat_id = message.chat.id,
                     text = 'Привет, {name} {emoji}!\n'
                            'Я Бот от туристического агентства Too Easy Travel!\n'
                            'Я помогу тебе выбрать место для отпуска по отличным ценам'.format(
                         name = message.from_user.username,
                         emoji = emoji.emojize(":wave:", use_aliases = True)
                     )
                     )
    logging.info(f'Бот отправил сообщение "{message.text}"')


@bot.message_handler(commands = ['hello_world'])
def send_welcome_to_the_world(message: telebot.types.Message):
    """
    Функция, которая реагирует на команду /hello_world и отправляет приветствие Пользователю.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    log_log(message)
    logging.info('Запущена команда /hello_world')
    bot.send_message(chat_id = message.chat.id,
                     text = 'Привет всему миру! {emoji}'.format(
                         emoji = emoji.emojize(":raised_hand:", use_aliases = True)
                     )
                     )
    logging.info(f'Бот отправил сообщение "{message.text}"')


@bot.message_handler(commands = ['lowprice'])
def low_price(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    log_log(message)
    logging.info('Запущена команда /lowprice')
    lowprice.start(message)


@bot.message_handler(content_types = ['text'])
def greeting(message: telebot.types.Message):
    """
    Функция, которая реагирует на приветствие пользователя чата либо отвечает что не знает такой команды.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message

    """
    log_log(message)
    logging.info('Запущена команда /text')
    logging.info(f'Пользователь написал "{message.text}"')
    if greeting_check(message):
        msg = bot.send_message(chat_id = message.chat.id,
                               text = 'И тебе привет, мой друг!')
        logging.info(f'Бот ответил "{msg.text}"')
    
    else:
        msg = bot.send_message(chat_id = message.chat.id,
                               text = 'Такого я еще не понимаю')
        logging.info(f'Бот ответил "{msg.text}"')

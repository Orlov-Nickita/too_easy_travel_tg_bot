import re
import emoji
import telebot.types
import lowprice
from loader import bot


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


print('Бот активирован')


@bot.message_handler(commands = ['start'])
def send_welcome(message: telebot.types.Message) -> None:
    """
    Функция, которая реагирует на команду /start при запуске бота и отправляет Пользователю приветствие
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    bot.send_message(chat_id = message.chat.id,
                     text = 'Привет, {name} {emoji}!\n'
                            'Я Бот от туристического агентства Too Easy Travel!\n'
                            'Я помогу тебе выбрать место для отпуска по отличным ценам'.format(
                                            name = message.from_user.username,
                                            emoji = emoji.emojize(":wave:", use_aliases = True)
                                            )
                     )
    

@bot.message_handler(commands = ['hello_world'])
def send_welcome_to_the_world(message: telebot.types.Message):
    """
    Функция, которая реагирует на команду /hello_world и отправляет приветствие Пользователю.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message
    
    """
    bot.send_message(chat_id = message.chat.id,
                     text = 'Привет всему миру! {emoji}'.format(
                         emoji = emoji.emojize(":raised_hand:", use_aliases = True)
                         )
                     )


@bot.message_handler(commands = ['lowprice'])
def low_price(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
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
    if greeting_check(message):
        bot.send_message(chat_id = message.chat.id,
                         text = 'И тебе привет, мой друг!')
    else:
        bot.send_message(chat_id = message.chat.id,
                         text = 'Такого я еще не понимаю')

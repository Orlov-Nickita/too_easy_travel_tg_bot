import telebot
import re

def greeting_check(greeting_message):
    if re.fullmatch(r'.риве.\S?', greeting_message.text):
        return True
    else:
        return False


print('ok')

bot = telebot.TeleBot('5097875553:AAGR3Mt8vaLxy6ny8n7uGSLQy_AUUFGOltM')


@bot.message_handler(commands = ['start'])
def send_welcome(message):
    """
    Функция, которая реагирует на команду /start при запуске бота
    :param message: В качестве параметра передается сообщение из чата
    :return: Возвращается приветствие
    :rtype str
    """
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username}!\n'
                                      f'Я Бот от туристического агентства Too Easy Travel!\nЯ помогу тебе '
                                      'выбрать место для отпуска по отличным ценам')


@bot.message_handler(commands = ['hello_world'])
def send_welcome_to_the_world(message):
    """
    Функция, которая реагирует на команду /hello_world при запуске бота
    :param message: В качестве параметра передается сообщение из чата
    :return: Возвращается приветствие
    :rtype str
    """
    bot.send_message(message.chat.id, 'Привет всему миру!')

@bot.message_handler(content_types = ['text'])
def greeting(message):
    """
    Функция, которая реагирует на приветствие пользователя чата
    :param message: В качестве параметра передается сообщение из чата
    :return: Возвращается приветствие
    :rtype str

    """
    if greeting_check(message):
        bot.send_message(message.chat.id, 'И тебе привет, мой друг!')
    else:
        bot.send_message(message.chat.id, 'Такого я еще не понимаю')


if __name__ == '__main__':
    bot.infinity_polling()
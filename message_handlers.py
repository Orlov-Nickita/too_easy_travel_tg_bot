import telebot.types
from commands_and_keyboards import text, hello_world, start, command, history, settings, help_command
from loader import bot, User_search
from utils.languages_for_bot import lang_dict
from utils.logger import log_log, logger
from utils.sqlite_history import history_data_add


@bot.message_handler(commands=['start'])
def send_welcome_func(message: telebot.types.Message) -> None:
    """
    Функция, которая реагирует на команду /start при запуске бота и отправляет Пользователю приветствие
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    log_log(message.from_user.username, message.chat.id)
    # logger = log_log(message.from_user.username, message.chat.id)
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log1'])
    User_search().get_user(user_id=message.chat.id).lang = message.from_user.language_code
    start.start(message)


@bot.message_handler(commands=['help'])
def help_command_func(message: telebot.types.Message) -> None:
    """
    Функция, которая реагирует на команду /help и отправляет Пользователю вспомогательное сообщение с подсказками
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype telebot.types.Message

    """
    log_log(message.from_user.username, message.chat.id)
    # logger = log_log(message.from_user.username, message.chat.id)

    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log9'])
    help_command.start(message)


@bot.message_handler(commands=['hello_world'])
def hello_world_func(message: telebot.types.Message):
    """
    Функция, которая реагирует на команду /hello_world и отправляет приветствие Пользователю.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    log_log(message.from_user.username, message.chat.id)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log2'])
    hello_world.start(message)


@bot.message_handler(commands=['lowprice'])
def low_price_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    log_log(message.from_user.username, message.chat.id)
    
    history_data_add(sql_base='user_database.db', user_id=message.chat.id, message_id=message.id,
                     msg_content=message.text)

    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log3'])
    User_search().get_user(user_id=message.chat.id).sort = 'PRICE'
    command.start(message)


@bot.message_handler(commands=['highprice'])
def high_price_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /highprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /highprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    log_log(message.from_user.username, message.chat.id)
    
    history_data_add(sql_base='user_database.db', user_id=message.chat.id, message_id=message.id,
                     msg_content=message.text)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log4'])
    User_search().get_user(user_id=message.chat.id).sort = 'PRICE_HIGHEST_FIRST'
    command.start(message)


@bot.message_handler(commands=['bestdeal'])
def bestdeal_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /bestdeal и поиска отелей в городе по заданным диапазонам
    цен и расстоянию от центра
    :param message: В качестве параметра передается сообщение с командой /bestdeal
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    log_log(message.from_user.username, message.chat.id)
    
    history_data_add(sql_base='user_database.db', user_id=message.chat.id, message_id=message.id,
                     msg_content=message.text)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log8'])
    User_search().get_user(user_id=message.chat.id).sort = 'DISTANCE_FROM_LANDMARK'
    command.start(message)


@bot.message_handler(commands=['history'])
def history_func(message: telebot.types.Message) -> None:
    """
    Задекорированная функция для запуска скрипта по команде /lowprice и поиска самых дешевых отелей в городе
    :param message: В качестве параметра передается сообщение с командой /lowprice
    :type message: telebot.types.Message
    :return: None
    :rtype: telebot.types.Message
    """
    log_log(message.from_user.username, message.chat.id)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log7'])
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
    log_log(message.from_user.username, message.chat.id)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log5'])
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
    log_log(message.from_user.username, message.chat.id)
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['message_handlers_logging']['log6'])
    text.start(message)

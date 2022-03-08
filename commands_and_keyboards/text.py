import telebot

from loader import bot, User_search
from useful_add_func.auxiliary_functions import greeting_check
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая формирует ответ на текстовое сообщение Пользователя
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message
    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log1'].format(
        message.text),
        username=message.from_user.username,
        user_id=message.chat.id)
    if greeting_check(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text'][
                                   'text1'])
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log2'].format(
            msg.text),
            user_id=message.chat.id)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text'][
                                   'text2'])
        
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log2'].format(
            msg.text),
            user_id=message.chat.id)

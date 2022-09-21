import telebot
import emoji
from loader import bot, User_search
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая формирует стартовое приветственное сообщение и отправляет Пользователю
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message
    
    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['start_logging']['log1'],
                username=message.from_user.username,
                user_id=message.chat.id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['start'][
                               'text1'].format(
                               name=message.from_user.username,
                               emoji=emoji.emojize(':wave:', language='alias')
                           )
                           )
    
    logger.info(
        lang_dict[User_search().get_user(user_id=message.chat.id).lang]['start_logging']['log2'].format(msg.text),
        user_id=message.chat.id)

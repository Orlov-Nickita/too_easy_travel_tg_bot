import telebot
import emoji
from loader import bot, User_search
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая формирует сообщение и отправляет приветствие Пользователю.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['hello_world_logging']['log1'],
                username=message.from_user.username,
                user_id=message.chat.id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['hello_world'][
                               'text1'].format(
                               emoji=emoji.emojize(":raised_hand:", use_aliases=True))
                           )
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['hello_world_logging']['log2'].format(
        msg=msg.text),
                user_id=message.chat.id)

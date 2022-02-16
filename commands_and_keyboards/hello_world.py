import logging
import telebot
import emoji
from my_bot.loader import bot, search
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая формирует сообщение и отправляет приветствие Пользователю.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    logging.info(lang_dict[search.lang]['hello_world_logging']['log1'], extra=search.user_id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['hello_world']['text1'].format(
                               emoji=emoji.emojize(":raised_hand:", use_aliases=True))
                           )
    logging.info(lang_dict[search.lang]['hello_world_logging']['log2'].format(msg=msg.text), extra=search.user_id)

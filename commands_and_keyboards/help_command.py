import logging
import telebot

from my_bot.loader import bot, search
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['help_command_logging']['log1'], extra=search.user_id)
    msg = bot.send_message(chat_id=message.chat.id, text=lang_dict[search.lang]['help_command']['text1'])

    logging.info(lang_dict[search.lang]['help_command_logging']['log2'].format(msg.text), extra=search.user_id)

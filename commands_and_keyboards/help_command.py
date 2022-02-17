import telebot

from loader import bot, search
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    logger.info(lang_dict[search.lang]['help_command_logging']['log1'])
    msg = bot.send_message(chat_id=message.chat.id, text=lang_dict[search.lang]['help_command']['text1'])

    logger.info(lang_dict[search.lang]['help_command_logging']['log2'].format(msg.text))

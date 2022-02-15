import logging
import telebot
from loader import bot
from auxiliary_functions import greeting_check
from utils.languages_for_bot import lang_dict
from loader import search


def start(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['text_logging']['log1'].format(message.text))
    if greeting_check(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['text']['text1'])
        logging.info(lang_dict[search.lang]['text_logging']['log2'].format(msg.text))
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['text']['text2'])

        logging.info(lang_dict[search.lang]['text_logging']['log2'].format(msg.text))

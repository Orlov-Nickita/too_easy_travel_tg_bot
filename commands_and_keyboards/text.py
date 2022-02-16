import logging
import telebot
from my_bot.loader import bot, search
from useful_add_func.auxiliary_functions import greeting_check
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['text_logging']['log1'].format(message.text), extra=search.user_id)
    if greeting_check(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['text']['text1'])
        logging.info(lang_dict[search.lang]['text_logging']['log2'].format(msg.text), extra=search.user_id)
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[search.lang]['text']['text2'])

        logging.info(lang_dict[search.lang]['text_logging']['log2'].format(msg.text), extra=search.user_id)

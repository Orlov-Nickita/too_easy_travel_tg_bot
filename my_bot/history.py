import logging
import telebot
import telegram

from languages_for_bot import lang_dict
from loader import bot, search
from sqlite import data_select


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая отправляет в чат историю запросов Пользователем.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    logging.info(lang_dict[search.lang]['history_logging']['log1'])
    
    history = data_select(sql_base='user_database.db', bot_user_id=message.chat.id)
    for every in history:
        if '/lowprice' in every[1] or '/highprice' in every[1] or '/bestdeal' in every[1]:
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=lang_dict[search.lang]['history']['text1'].format(com=every[1],
                                                                                          dt=every[2],
                                                                                          tm=every[3]),
                                   parse_mode=telegram.ParseMode.HTML)
            
            logging.info(lang_dict[search.lang]['history_logging']['log2'].format(msg.text))
        
        else:
            bot.forward_message(chat_id=message.chat.id,
                                from_chat_id=message.chat.id,
                                message_id=every[0])
            
            logging.info(lang_dict[search.lang]['history_logging']['log3'])

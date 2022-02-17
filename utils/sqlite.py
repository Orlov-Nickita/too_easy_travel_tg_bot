import logging
import sqlite3 as sq
import datetime

from utils.languages_for_bot import lang_dict
from loader import search, bot


def data_add(sql_base: str, user_id: int, message_id: int, msg_content: str) -> None:
    logging.info(lang_dict[search.lang]['sqlite_logging']['log1'], extra=search.user_id)
    
    try:
        date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
        time_msg = datetime.datetime.today().strftime("%H:%M")
        
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS bot_users (
                user_id INTEGER,
                message_id INTEGER,
                message_content TEXT,
                date TEXT,
                time TEXT
                )""")
            
            cursor.execute(
                "INSERT INTO bot_users VALUES ({}, {}, '{}', '{}', '{}')".format(user_id, message_id, msg_content,
                                                                                 date_msg,
                                                                                 time_msg))
            
            logging.info(lang_dict[search.lang]['sqlite_logging']['log4'], extra=search.user_id)
    
    except Exception as Exec:
        logging.info(lang_dict[search.lang]['sqlite_logging']['log2'].format(Exec), extra=search.user_id)
        bot.send_message(chat_id=user_id, text=lang_dict[search.lang]['sqlite']['text1'])


def data_select(sql_base: str, bot_user_id: int) -> list:
    logging.info(lang_dict[search.lang]['sqlite_logging']['log3'], extra=search.user_id)
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            
            cursor.execute(
                "SELECT message_id, message_content, date, time FROM bot_users WHERE user_id == {}".format(bot_user_id))
            
            logging.info(lang_dict[search.lang]['sqlite_logging']['log5'], extra=search.user_id)
            
            result = cursor.fetchall()
            return result
    
    except Exception as Exec:
        logging.info(lang_dict[search.lang]['sqlite_logging']['log2'].format(Exec), extra=search.user_id)
        bot.send_message(chat_id=bot_user_id, text=lang_dict[search.lang]['sqlite']['text1'])

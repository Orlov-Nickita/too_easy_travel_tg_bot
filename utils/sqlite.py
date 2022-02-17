import sqlite3 as sq
import datetime

from utils.languages_for_bot import lang_dict
from loader import search, bot
from utils.logger import logger


def data_add(sql_base: str, user_id: int, message_id: int, msg_content: str) -> None:
    logger.info(lang_dict[search.lang]['sqlite_logging']['log1'])
    
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
            
            logger.info(lang_dict[search.lang]['sqlite_logging']['log4'])
    
    except Exception as Exec:
        logger.info(lang_dict[search.lang]['sqlite_logging']['log2'].format(Exec))
        bot.send_message(chat_id=user_id, text=lang_dict[search.lang]['sqlite']['text1'])


def data_select(sql_base: str, bot_user_id: int) -> list:
    logger.info(lang_dict[search.lang]['sqlite_logging']['log3'])
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            
            cursor.execute(
                "SELECT message_id, message_content, date, time FROM bot_users WHERE user_id == {}".format(bot_user_id))
            
            logger.info(lang_dict[search.lang]['sqlite_logging']['log5'])
            
            result = cursor.fetchall()
            return result
    
    except Exception as Exec:
        logger.info(lang_dict[search.lang]['sqlite_logging']['log2'].format(Exec))
        bot.send_message(chat_id=bot_user_id, text=lang_dict[search.lang]['sqlite']['text1'])

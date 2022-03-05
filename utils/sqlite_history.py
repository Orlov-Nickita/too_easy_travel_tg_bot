import sqlite3 as sq
import datetime

from utils.languages_for_bot import lang_dict
from loader import bot, User_search
from utils.logger import logger


def history_data_add(sql_base: str, user_id: int, message_id: int, msg_content: str) -> None:
    """
    Функция, которая добавляет в базу данных информацию. Первоначально проверяет не создана ли уже база данных и
    создает ее, если она не создана, а если ранее уже была создана, то сразу добавляет туда информацию
    :param sql_base: Название базы данных, с которой необходимо будет работать
    :type sql_base: str
    :param user_id: ID Пользователя, для которого добавляется информация в базу данных
    :type user_id: int
    :param message_id: ID сообщения, которое сохраняется в базу данных
    :type message_id: int
    :param msg_content: Текстовое описание того, что сохраняется в базу данных: фотография или информация об отеле
    :type msg_content: str
    """
    logger.info(lang_dict[User_search().get_user(user_id=user_id).lang]['sqlite_history_logging']['log1'],
                user_id=user_id)
    
    try:
        date_msg = datetime.datetime.today().strftime("%d.%m.%Y")
        time_msg = datetime.datetime.today().strftime("%H:%M")
        
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS users_history (
                user_id INTEGER,
                message_id INTEGER,
                message_content TEXT,
                date TEXT,
                time TEXT
                )""")
            
            cursor.execute(
                "INSERT INTO users_history VALUES ({}, {}, '{}', '{}', '{}')".format(user_id, message_id, msg_content,
                                                                                     date_msg,
                                                                                     time_msg))
            
            logger.info(lang_dict[User_search().get_user(user_id=user_id).lang]['sqlite_history_logging']['log4'],
                        user_id=user_id)
    
    except Exception as Exec:
        logger.info(
            lang_dict[User_search().get_user(user_id=user_id).lang]['sqlite_history_logging']['log2'].format(Exec),
            user_id=user_id)
        bot.send_message(chat_id=user_id,
                         text=lang_dict[User_search().get_user(user_id=user_id).lang]['sqlite_history']['text1'])


def history_data_select(sql_base: str, bot_user_id: int) -> list:
    """
    Функция, которая добавляет в базу данных информацию. Первоначально проверяет не создана ли уже база данных и
    создает ее, если она не создана, а если ранее уже была создана, то сразу добавляет туда информацию
    :param sql_base: Название базы данных, с которой необходимо будет работать
    :type sql_base: str
    :param bot_user_id: ID Пользователя, для которого добавляется информация в базу данных
    :type bot_user_id: int
    
    """
    logger.info(lang_dict[User_search().get_user(user_id=bot_user_id).lang]['sqlite_history_logging']['log3'],
                user_id=bot_user_id)
    
    try:
        with sq.connect(sql_base) as database:
            cursor = database.cursor()
            
            cursor.execute(
                "SELECT message_id, message_content, date, time FROM users_history WHERE user_id == {}".format(
                    bot_user_id))
            
            logger.info(lang_dict[User_search().get_user(user_id=bot_user_id).lang]['sqlite_history_logging']['log5'],
                        user_id=bot_user_id)
            
            result = cursor.fetchall()
            return result
    
    except Exception as Exec:
        logger.info(
            lang_dict[User_search().get_user(user_id=bot_user_id).lang]['sqlite_history_logging']['log2'].format(Exec),
            user_id=bot_user_id)
        bot.send_message(chat_id=bot_user_id,
                         text=lang_dict[User_search().get_user(user_id=bot_user_id).lang]['sqlite_history']['text1'])

import telebot
from loader import bot, User_search
from useful_add_func.auxiliary_functions import greeting_check
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log1'].format(
        message.text))
    if greeting_check(message):
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text'][
                                   'text1'])
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log2'].format(
            msg.text))
    
    else:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text'][
                                   'text2'])
        
        logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['text_logging']['log2'].format(
            msg.text))

import logging
import telebot
import emoji

from loader import bot, search
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    logging.info(lang_dict[search.lang]['start_logging']['log1'], extra=search.user_id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['start']['text1'].format(
                               name=message.from_user.username,
                               emoji=emoji.emojize(":wave:", use_aliases=True)
                           )
                           )

    logging.info(lang_dict[search.lang]['start_logging']['log2'].format(msg.text), extra=search.user_id)

import telebot
import emoji
import telegram

from useful_add_func.auxiliary_functions import button_text
from loader import bot, User_search
from commands_and_keyboards.keyboards import IKM_for_settings, IKM_settings_lang, IKM_settings_currency
from utils.languages_for_bot import lang_dict
from utils.logger import logger


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая отправляет в чат "Меню бота" с возможностью изменить язык бота и валюту.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id).lang]['settings_logging']['log1'],
                username=message.from_user.username,
                user_id=message.chat.id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[User_search().get_user(user_id=message.chat.id
                                                                 ).lang]['settings']['text1'].format(
                               emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                           reply_markup=IKM_for_settings(message),
                           parse_mode=telegram.ParseMode.HTML
                           )
    
    logger.info(lang_dict[User_search().get_user(user_id=message.chat.id
                                                 ).lang]['settings_logging']['log2'].format(msg.text),
                user_id=message.chat.id)


# Реакция в главном меню
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings']['text01']))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_settings
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: В зависимости нажатой клавиши происходит переход либо к функции изменения языка или изменения валюты
    :rtype: None
    """
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings_logging']['log3'],
                username=call.message.from_user.username,
                user_id=call.message.chat.id)
    
    if call.data == 'language':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[User_search().get_user(
                                        user_id=call.message.chat.id).lang]['settings']['text2'].format(
                                        emoji=emoji.emojize(":open_file_folder:", use_aliases=True)),
        
                                    reply_markup=IKM_settings_lang(call.message),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log2'].format(msg.text),
                    user_id=call.message.chat.id)
    
    elif call.data == 'currency':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                          ).lang]['settings']['text3'].format(
                                        emoji=emoji.emojize(":open_file_folder:", use_aliases=True),
                                        emoji1=emoji.emojize(":currency_exchange:", use_aliases=True)),
        
                                    reply_markup=IKM_settings_currency(call.message),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log2'].format(msg.text),
                    user_id=call.message.chat.id)
    
    elif call.data == 'close':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# Выбор языка
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings']['text02']))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопку клавиатуры IKM_settings_lang выбора языка
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: Сообщение изменяется и появляется возможность выбора языка или возврата в главное меню
    :rtype: None
    """
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings_logging']['log5'],
                username=call.message.from_user.username,
                user_id=call.message.chat.id)
    
    if call.data == 'mainmenu':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[User_search().get_user(
                                        user_id=call.message.chat.id).lang]['settings']['text1'].format(
                                        emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                                    reply_markup=IKM_for_settings(call.message),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log2'].format(msg.text),
                    user_id=call.message.chat.id)
    
    elif call.data == 'close':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'ru' or call.data == 'en':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log7'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=lang_dict[User_search().get_user(
                                      user_id=call.message.chat.id
                                  ).lang]['settings']['text4'].format(lan=button_text(call)))
        User_search().get_user(user_id=call.message.chat.id).lang = call.data
        User_search().users[call.message.chat.id].lang = call.data
        
        if call.data == 'ru':
            User_search().get_user(user_id=call.message.chat.id).locale = 'ru_RU'
        elif call.data == 'en':
            User_search().get_user(user_id=call.message.chat.id).locale = 'en_US'
        
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                    ).lang]['settings']['text2'].format(
                                  emoji=emoji.emojize(":open_file_folder:", use_aliases=True)),
        
                              reply_markup=IKM_settings_lang(call.message),
                              parse_mode=telegram.ParseMode.HTML)


# Выбор валюты
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings']['text03'].format(
        emoji1=emoji.emojize(":currency_exchange:", use_aliases=True))))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопку клавиатуры IKM_settings_currency выбора валюты
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: Сообщение изменяется и появляется возможность выбора валюты или возврата в главное меню
    :rtype: None
    """
    
    logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id).lang]['settings_logging']['log6'],
                username=call.message.from_user.username,
                user_id=call.message.chat.id)
    
    if call.data == 'mainmenu':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                                          ).lang]['settings']['text1'].format(
                                        emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                                    reply_markup=IKM_for_settings(call.message),
                                    parse_mode=telegram.ParseMode.HTML)
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log2'].format(msg.text),
                    user_id=call.message.chat.id)
    
    elif call.data == 'close':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log4'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'RUB' or call.data == 'USD' or call.data == 'EUR':
        logger.info(lang_dict[User_search().get_user(user_id=call.message.chat.id
                                                     ).lang]['settings_logging']['log8'].format(button_text(call)),
                    user_id=call.message.chat.id)
        
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=lang_dict[User_search().get_user(
                                      user_id=call.message.chat.id
                                  ).lang]['settings']['text5'].format(cur=button_text(call)))
        User_search().get_user(user_id=call.message.chat.id).currency = call.data

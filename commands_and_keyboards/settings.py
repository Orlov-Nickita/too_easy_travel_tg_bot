import logging
import telebot
import emoji
import telegram

from useful_add_func.auxiliary_functions import button_text
from loader import bot, search
from commands_and_keyboards.keyboards import IKM_for_settings, IKM_settings_lang, IKM_settings_currency
from utils.languages_for_bot import lang_dict


def start(message: telebot.types.Message) -> None:
    """
    Функция, которая отправляет в чат "Меню бота" с возможностью изменить язык бота и валюту.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :return: Отправляется сообщение в чат
    :rtype: telebot.types.Message

    """
    logging.info(lang_dict[search.lang]['settings_logging']['log1'], extra=search.user_id)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=lang_dict[search.lang]['settings']['text1'].format(
                               emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                           reply_markup=IKM_for_settings(),
                           parse_mode=telegram.ParseMode.HTML
                           )
    
    logging.info(lang_dict[search.lang]['settings_logging']['log2'].format(msg.text), extra=search.user_id)


# Реакция в главном меню
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[search.lang]['settings']['text01']))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопки клавиатуры IKM_for_settings
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: В зависимости нажатой клавиши происходит переход либо к функции изменения языка или изменения валюты
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['settings_logging']['log3'], extra=search.user_id)
    
    if call.data == 'language':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[search.lang]['settings']['text2'].format(
                                        emoji=emoji.emojize(":open_file_folder:", use_aliases=True)),
        
                                    reply_markup=IKM_settings_lang(),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logging.info(lang_dict[search.lang]['settings_logging']['log2'].format(msg.text), extra=search.user_id)
    
    elif call.data == 'currency':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[search.lang]['settings']['text3'].format(
                                        emoji=emoji.emojize(":open_file_folder:", use_aliases=True),
                                        emoji1=emoji.emojize(":currency_exchange:", use_aliases=True)),
        
                                    reply_markup=IKM_settings_currency(),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logging.info(lang_dict[search.lang]['settings_logging']['log2'].format(msg.text), extra=search.user_id)
    
    elif call.data == 'close':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# Выбор языка
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[search.lang]['settings']['text02']))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопку клавиатуры IKM_settings_lang выбора языка
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: Сообщение изменяется и появляется возможность выбора языка или возврата в главное меню
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['settings_logging']['log5'], extra=search.user_id)
    
    if call.data == 'mainmenu':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[search.lang]['settings']['text1'].format(
                                        emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                                    reply_markup=IKM_for_settings(),
                                    parse_mode=telegram.ParseMode.HTML)
        
        logging.info(lang_dict[search.lang]['settings_logging']['log2'].format(msg.text), extra=search.user_id)
    
    elif call.data == 'close':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'ru' or call.data == 'en':
        logging.info(lang_dict[search.lang]['settings_logging']['log7'].format(button_text(call)), extra=search.user_id)
        
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=lang_dict[search.lang]['settings']['text4'].format(lan=button_text(call)))
        search.lang = call.data
        
        if call.data == 'ru':
            search.locale = 'ru_RU'
        elif call.data == 'en':
            search.locale = 'en_US'
        
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=lang_dict[search.lang]['settings']['text2'].format(
                                  emoji=emoji.emojize(":open_file_folder:", use_aliases=True)),
        
                              reply_markup=IKM_settings_lang(),
                              parse_mode=telegram.ParseMode.HTML)


# Выбор валюты
@bot.callback_query_handler(func=lambda call: call.message.content_type == 'text' and call.message.text.endswith(
    lang_dict[search.lang]['settings']['text03'].format(emoji1=emoji.emojize(":currency_exchange:", use_aliases=True))))
def change_settings(call: telebot.types.CallbackQuery) -> None:
    """
    Функция, предназначенная для обработки нажатия на кнопку клавиатуры IKM_settings_currency выбора валюты
    :param call: В качестве параметра передается параметр callback_data нажатой клавиши.
    :type: telebot.types.CallbackQuery
    :return: Сообщение изменяется и появляется возможность выбора валюты или возврата в главное меню
    :rtype: None
    """
    
    logging.info(lang_dict[search.lang]['settings_logging']['log6'], extra=search.user_id)
    
    if call.data == 'mainmenu':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=lang_dict[search.lang]['settings']['text1'].format(
                                        emoji=emoji.emojize(":file_folder:", use_aliases=True)),
                                    reply_markup=IKM_for_settings(),
                                    parse_mode=telegram.ParseMode.HTML)
        logging.info(lang_dict[search.lang]['settings_logging']['log2'].format(msg.text), extra=search.user_id)
    
    elif call.data == 'close':
        logging.info(lang_dict[search.lang]['settings_logging']['log4'].format(button_text(call)), extra=search.user_id)
        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'RUB' or call.data == 'USD' or call.data == 'EUR':
        logging.info(lang_dict[search.lang]['settings_logging']['log8'].format(button_text(call)), extra=search.user_id)
        
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=lang_dict[search.lang]['settings']['text5'].format(cur=button_text(call)))
        search.currency = call.data

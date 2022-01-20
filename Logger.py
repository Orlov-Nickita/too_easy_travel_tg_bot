import telebot
import logging


def log_log(message: telebot.types.Message) -> None:
    """
    Функция для конфигурации логгера. Когда запускается функция, параметром является объект сообщения, содержащий
    id Пользователя для создания одноименного файла с журналом событий
    :param message: Параметром является сообщение
    :type message: telebot.types.Message
    :return: None
    """
    logging.basicConfig(filename = 'logs/{user_id} - {user}.log'.format(user_id = message.from_user.id,
                                                                        user = message.from_user.username),
                        level = logging.INFO,
                        encoding = 'utf-8',
                        format = '[%(levelname)s] - '
                                 '[%(asctime)s] - '
                                 '[файл %(filename)s] - '
                                 '[функция %(funcName)s] - '
                                 '[строка %(lineno)d] - '
                                 '[%(message)s]'
                        )

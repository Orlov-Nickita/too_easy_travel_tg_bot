import logging


# def log_log() -> None:
#     """
#     Функция для конфигурации логгера. Когда запускается функция, параметром является объект сообщения, содержащий
#     id Пользователя для создания одноименного файла с журналом событий
#     :return: None
#     """
logging.basicConfig(filename='../logs/bot_detail.log',
                    level=logging.INFO,
                    encoding='utf-8',
                    format='[%(user)s] - '
                           '[%(levelname)s] - '
                           '[%(asctime)s] - '
                           '[file %(filename)s] - '
                           '[func %(funcName)s] - '
                           '[num_string %(lineno)d] - '
                           '[%(message)s]',
                    )

logger = logging.getLogger()

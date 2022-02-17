import logging


def log_log(username, userid):
    logging.basicConfig(filename='logs/bot_detail.log',
                        level=logging.INFO,
                        encoding='utf-8',
                        format='[username {}] - '
                               '[userid {}] - '
                               '[%(levelname)s] - '
                               '[%(asctime)s] - '
                               '[file %(filename)s] - '
                               '[func %(funcName)s] - '
                               '[num_string %(lineno)d] - '
                               '[%(message)s]'.format(username, userid)
                        )


logger = logging.getLogger('logger')

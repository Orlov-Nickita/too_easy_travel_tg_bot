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

# TODO поправить логгер чтобы корректно воспринимал двух пользователей, убрать basicConfig

#
# def log_log(username, userid):
#
#     logger2 = logging.getLogger('logger2')
#     format_log = '[username {}] - [userid {}] - [%(levelname)s] - [%(asctime)s] - [file %(filename)s] - ' \
#                  '[func %(funcName)s] - [num_string %(lineno)d] - [%(message)s]'.format(username, userid)
#     logger2.setLevel(logging.INFO)
#     fh = logging.FileHandler(filename='logs/bot_detail.log', encoding='utf-8')
#     fh.setFormatter(logging.Formatter(format_log))
#     fh.setLevel(logging.INFO)
#     logger2.addHandler(fh)
#     return logger2
#
# #
# logger = ''
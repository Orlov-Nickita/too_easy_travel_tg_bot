import logging

logger_main = logging.getLogger('logger_main')
format_log = '[] - [] - [%(levelname)s] - [%(asctime)s] - [file %(filename)s] - ' \
             '[func %(funcName)s] - [num_string %(lineno)d] - [%(message)s]'
logger_main.setLevel(logging.INFO)
fh = logging.FileHandler(filename='logs/bot_detail.log', encoding='utf-8')
fh.setFormatter(logging.Formatter(format_log))
fh.setLevel(logging.INFO)
logger_main.addHandler(fh)
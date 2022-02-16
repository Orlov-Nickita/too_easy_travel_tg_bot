import logging

logging.basicConfig(filename='../logs/bot_detail.log',
                    level=logging.INFO,
                    encoding='utf-8',
                    format='[%(username)s] - '
                           '[%(userid)s] - '
                           '[%(levelname)s] - '
                           '[%(asctime)s] - '
                           '[file %(filename)s] - '
                           '[func %(funcName)s] - '
                           '[num_string %(lineno)d] - '
                           '[%(message)s]',
                    )

logger = logging.getLogger()

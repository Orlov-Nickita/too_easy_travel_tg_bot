import os.path

from message_handlers import *
from utils.logger import logger

if __name__ == '__main__':
    if not os.path.exists("../logs/"):
        os.makedirs("../logs/")
    
    logger.info('the log message', extra={'user': 'Jane'})
    
    bot.infinity_polling()

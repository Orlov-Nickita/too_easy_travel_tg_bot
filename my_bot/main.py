import os.path

from my_bot.message_handlers import *
from utils.logger import logger

if __name__ == '__main__':
    if not os.path.exists("../logs/"):
        os.makedirs("../logs/")
    
    logger.info(lang_dict[search.lang]['main_logging']['log1'], extra={'username': '', 'userid': ''})
    
    bot.infinity_polling()

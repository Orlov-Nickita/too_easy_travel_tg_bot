import os.path

from logger import log_log
from message_handlers import *

if __name__ == '__main__':
    if not os.path.exists("../logs/"):
        os.makedirs("../logs/")
    
    log_log()
    logging.info(lang_dict[search.lang]['main_logging']['log1'])
    
    bot.infinity_polling()

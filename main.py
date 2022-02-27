import os.path
from message_handlers import *
from utils.logger_main import logger_main

if __name__ == '__main__':
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    
    logger_main.info(lang_dict['ru']['main_logging']['log1'] + ' | ' + lang_dict['en']['main_logging']['log1'] )
    
    bot.infinity_polling()

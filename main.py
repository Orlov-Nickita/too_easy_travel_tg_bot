import os
import os.path
from message_handlers import *

if __name__ == '__main__':
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    
    log_log()
    logging.info('Бот запущен')
    
    bot.infinity_polling()

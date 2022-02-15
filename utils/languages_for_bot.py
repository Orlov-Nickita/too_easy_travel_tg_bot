"""
Языковая поддержка Бота. Заранее определенные соответствующему языку фразы для журнала событий и для Пользователя
"""

lang_dict = {
    'ru': {
        'keyboards': {
            'IKM_for_greeting_msg': {
                'text1': '{}',
                'text2': 'Выбрать другой город'
            },
            'IKM_for_city_choice': {
                'text1': 'Вернуться назад'
            },
            'IKM_for_hotels_poisk': {
                'text1': 'Вернуться назад'
            },
            'IKM_for_photos_search': {
                'text1': 'Да',
                'text2': 'Нет',
                'text3': 'Вернуться назад'
            },
            'IKM_photos_sliding': {
                'text1': '< Листать фото',
                'text2': 'Листать фото >'
            },
            'IKM_date_chk_in_change': {
                'text1': 'Изменить дату',
                'text2': 'Далее'
            },
            'IKM_date_chk_out_change': {
                'text1': 'Изменить дату',
                'text2': 'Далее'
            },
            'IKM_for_settings': {
                'text1': 'Сменить язык',
                'text2': 'Сменить валюту'
            },
            'IKM_settings_lang': {
                'text1': 'Русский',
                'text2': 'Английский',
                'text3': 'Главное меню'
            },
            'IKM_settings_currency': {
                'text1': '{emoji1} Рубль',
                'text2': '{emoji2} Доллар',
                'text3': '{emoji3} Евро',
                'text4': 'Главное меню'
            },
            'IKM_price_distance_approve': {
                'text1': 'Изменить',
                'text2': 'Далее'
            }
        },
        'hello_world': {
            'text1': 'Привет всему миру! {emoji}'
        },
        'hello_world_logging': {
            'log1': 'Запущена функция hello_world.start',
            'log2': 'Бот отправил сообщение "{msg}"'
        },
        'command': {
            'text1': 'Ваше местоположение город {city}.\nХотите поменять город поиска или ищем по месту нахождения?',
            'text1.1': 'Ваше местоположение город',
            'text2': 'В каком городе будем искать отели?',
            'text3': 'Хороший выбор, ищу город {city} на карте',
            'text4': 'Вот, что мне удалось найти по запросу - город {city}.\nНажмите кнопку соответствующую Вашему '
                     'запросу',
            'text4.1': 'Вот, что мне удалось найти по запросу - город',
            'text5': 'Выберите дату въезда',
            'text6': 'Вы выбрали дату въезда {res}',
            'text6.1': 'Вы выбрали дату въезда',
            'text7': 'Выберите дату выезда',
            'text8': 'Вы выбрали дату выезда {res}',
            'text8.1': 'Вы выбрали дату выезда',
            'text9': 'Дата выезда не может совпадать с датой въезда. Минимальный срок бронирования отеля составляет '
                     '1 сутки. Пожалуйста, выберите дату выезда еще раз',
            'text10': 'Итак, какое количество отелей подобрать?',
            'text11': 'Потребуются ли фотографии для ознакомления?',
            'text12': '{emoji1} Название отеля: <b>{hotel_name}</b>\n'
                      '{emoji2} Веб-сайт отеля: <a>{web}</a>\n'
                      '{emoji3} Адрес: <code>{address}</code>\n'
                      '{emoji4} Открыть Яндекс карты: <a>{yamaps}</a>\n'
                      '{emoji5} Удаленность от центра: <code>{center}</code>\n'
                      '{emoji6} Цена за весь период: <code>{price}</code>\n'
                      '{emoji7} Дата въезда: <code>{chk_in_date}</code>\n'
                      '{emoji8} Дата выезда: <code>{chk_out_date}</code>\n'
                      '{emoji9} Цена за сутки: <code>{one_day_price}</code>\n'
                      '{emoji10} Рейтинг: <code>{rating}</code>\n'
                      '{emoji11} Рейтинг по мнению посетителей: <code>{user_rating}</code>\n',
            'text13': 'Укажите допустимый диапазон цен за проживание в отеле через пробел',
            'text14': 'Укажите допустимый диапазон расстояния в метрах, на котором может находиться отель '
                      'от центра через пробел',
            'text15': 'Вы выбрали диапазон цен от {} руб. до {} руб.',
            'text15.1': 'Вы выбрали диапазон цен от',
            'text16': 'Вы выбрали желаемое расстояние от центра города от {} метров до {} метров',
            'text16.1': 'Вы выбрали желаемое расстояние от центра города от',
            'text17': 'По Вашему запросу не удалось ничего найти. Попробуйте изменить параметры поиска',
            'text18': 'Ошибка ввода данных. Диапазон цен необходимо написать через пробел',
            'text19': 'Ошибка ввода данных. Диапазон расстояния необходимо написать через пробел'
            
        },
        'command_logging': {
            'log1': 'Запущена функция command.start с определением местоположения Пользователя',
            'log2': 'Бот определил местоположение Пользователя в городе "{city}"',
            'log3': 'Бот отправил сообщение "{msg}"',
            'log4': 'Пользователь нажал на кнопку "{button}" и выбрал текущее местоположение',
            'log5': 'Пользователь нажал на кнопку "{button}" и предпочел выбрать другой город для поиска',
            'log6': 'Запущена функция city_choice',
            'log7': 'Бот отправил сообщение "{msg}"',
            'log8': 'Запущена функция city_poisk',
            'log9': 'Бот отправил сообщение "{msg2}", {cities}',
            'log10': 'Пользователь выбрал место поиска "{button}"',
            'log11': 'Запущена функция city_choice_keyboard_callback',
            'log12': 'Запущена функция check_in_date_choice',
            'log13': 'Запущена функция chk_in_date_calendar',
            'log14': 'Пользователь выбрал дату въезда {time_res}',
            'log15': 'Запущена функция chk_in_date_change',
            'log16': 'Пользователь нажал на кнопку "{button}"',
            'log17': 'Запущена функция check_out_date_choice',
            'log18': 'Запущена функция chk_out_date_calendar',
            'log19': 'Пользователь выбрал дату выезда {time_res} такую же как дату въезда. Бот включил уведомление '
                     'об ошибке',
            'log20': 'Пользователь выбрал дату выезда {time_res}',
            'log21': 'Запущена функция chk_out_date_change',
            'log22': 'Запущена функция qty_hotels',
            'log23': 'Запущена функция city_poisk_keyboard_callback',
            'log24': 'Запущена функция hotels_poisk_in_the_city',
            'log25': 'Запущена функция hotels_poisk_keyboard_callback',
            'log26': 'Запущена функция hotels_info',
            'log27': 'Бот отправил сообщение c информацией по отелю',
            'log28': 'Бот отправил фото',
            'log29': 'Запущена функция photo_slide - открыта клавиатура',
            'log30': 'Запущена функция price_range',
            'log31': 'Запущена функция price_limiter',
            'log32': 'Запущена функция distance_range',
            'log33': 'Запущена функция distance_limiter',
            'log34': 'Запущена функция price_limiter_approve',
            'log35': 'Запущена функция price_limiter_approve',
            'log36': 'Ведется поиск отелей на странице {}',
            'log37': 'Пользователь ввел диапазон цен с ошибкой',
            'log38': 'В функции price_limiter произошла ошибка {}',
            'log39': 'Пользователь ввел диапазон расстояния с ошибкой',
            'log40': 'В функции distance_limiter произошла ошибка {}',
    
        },
        'command_acq': {
            'acq1': 'Принято',
            'acq2': 'Выполняется поиск',
            'acq3': 'Ответ принят',
        },
        'command_print_search_info': {
            'key1': 'ID отеля',
            'key2': 'Адрес',
            'key3': 'Координаты',
            'key4': 'Удаленность от центра',
            'key5': 'Цена за весь период',
            'key6': 'Цена за 1 сутки',
            'key7': 'Рейтинг отеля',
            'key8': 'Рейтинг по мнению посетителей',
            'key9': 'Сайт'
        },
        'main_logging': {
            'log1': 'Бот запущен'
        },
        'message_handlers_logging': {
            'log1': 'Запущена команда /start',
            'log2': 'Запущена команда /hello_world',
            'log3': 'Запущена команда /lowprice',
            'log4': 'Запущена команда /highprice',
            'log5': 'Запущена команда /settings_func',
            'log6': 'Запущена команда /text',
            'log7': 'Запущена команда /history',
            'log8': 'Запущена команда /bestdeal',
            
        },
        'requests_rapidapiHotels_logging': {
            'city_search': {
                'log1': 'Запрос на сервер в функции city_poisk прошел успешно',
                'log2': 'Ответ с сервера в функции city_search превысил заданный тайм-аут',
                'log3': 'В функции city_poisk произошла ошибка {}'
            },
            'hotels_search_price': {
                'log1': 'Запрос на сервер в функции hotels_search_price прошел успешно',
                'log2': 'Ответ с сервера в функции hotels_search_price превысил заданный тайм-аут',
                'log3': 'В функции hotels_search_price произошла ошибка {}'
            },
            'photos_for_hotel': {
                'log1': 'Запрос на сервер в функции photos_for_hotel прошел успешно',
                'log2': 'Ответ с сервера в функции photos_for_hotel превысил заданный тайм-аут',
                'log3': 'В функции photos_for_hotel произошла ошибка {}'
            }
        },
        'requests_rapidapiHotels': {
            'text1': 'К сожалению не удалось получить информацию с сервера. Сделайте, пожалуйста, выбор еще раз'
        },
        'settings': {
            'text1': '{emoji} <b>Меню бота</b>\n'
                     'Данное меню позволяет изменить настройки',
            'text01': 'Данное меню позволяет изменить настройки',
            'text2': '{emoji} <b>Меню бота</b>\n'
                     'Выберите язык',
            'text02': 'Выберите язык',
            'text3': '{emoji} <b>Меню бота</b>\n'
                     'Выберите валюту {emoji1}',
            'text03': 'Выберите валюту {emoji1}',
            
            'text4': 'Выбран язык - {lan}',
            'text5': 'Выбрана валюта {cur}'
            
        },
        'settings_logging': {
            'log1': 'Запущена функция settings.start',
            'log2': 'Бот отправил сообщение "{}"',
            'log3': 'Запущена функция settings.change_settings при переходе из главного меню',
            'log4': 'Пользователь нажал на кнопку "{}"',
            'log5': 'Запущена функция settings.change_settings при переходе из меню выбора языка',
            'log6': 'Запущена функция settings.change_settings при переходе из меню выбора валюты',
            'log7': 'Пользователь нажал на кнопку "{}" и выбрал соответствующий язык',
            'log8': 'Пользователь нажал на кнопку "{}" и выбрал соответствующую валюту',
            
        },
        'text': {
            'text1': 'И тебе привет, мой друг!',
            'text2': 'Такого я еще не понимаю'
        },
        'text_logging': {
            'log1': 'Пользователь написал "{}"',
            'log2': 'Бот ответил "{}"'
        },
        'start': {
            'text1': 'Здравствуй, {name} {emoji}!\n'
                     'Я Бот от туристического агентства Too Easy Travel!\n'
                     'Я помогу Вам выбрать место для отпуска по отличным ценам'
        },
        'start_logging': {
            'log1': 'Запущена функция start.start',
            'log2': 'Бот отправил сообщение "{}"'
        },
        'history': {
            'text1': '<b>Вы отправили команду {com}. '
                     'Дата и время отправки команды {tm} {dt}</b>'
        },
        'history_logging': {
            'log1': 'Запущена функция history.start',
            'log2': 'Бот отправил сообщение "{}"',
            'log3': 'Бот переслал сообщение Пользователя',
            
        },
        'sqlite': {
            'text1': 'Произошла ошибка. Попробуйте, пожалуйста, еще раз. '
                     'Если ошибка повторится, обратитесь к Администратору'
        },
        'sqlite_logging': {
            'log1': 'Запущена команда sqlite.data_add',
            'log2': 'Произошла ошибка:\n{}',
            'log3': 'Запущена команда sqlite.data_select',
            'log4': 'В базу данных добавлена запись',
            'log5': 'Из базы данных получена запись/записи',
            
        },
    },
    'en': {
        'keyboards': {
            'IKM_for_greeting_msg': {
                'text1': '{}',
                'text2': 'Choose another city'
            },
            'IKM_for_city_choice': {
                'text1': 'Go back'
            },
            'IKM_for_hotels_poisk': {
                'text1': 'Go back'
            },
            'IKM_for_photos_search': {
                'text1': 'Yes',
                'text2': 'No',
                'text3': 'Go back'
            },
            'IKM_photos_sliding': {
                'text1': '< Scroll photos',
                'text2': 'Scroll photos >'
            },
            'IKM_date_chk_in_change': {
                'text1': 'Change date',
                'text2': 'Next step'
            },
            'IKM_date_chk_out_change': {
                'text1': 'Change date',
                'text2': 'Next step'
            },
            'IKM_for_settings': {
                'text1': 'Change language',
                'text2': 'Change currency'
            },
            'IKM_settings_lang': {
                'text1': 'Russian',
                'text2': 'English',
                'text3': 'Main menu'
            },
            'IKM_settings_currency': {
                'text1': '{emoji1} Ruble',
                'text2': '{emoji2} Dollar',
                'text3': '{emoji3} Euro',
                'text4': 'Main menu'
            },
            'IKM_price_distance_approve': {
                'text1': 'Change',
                'text2': 'Next step'
            }
        },
        'hello_world': {
            'text1': 'Hello to the whole world! {emoji}'
        },
        'hello_world_logging': {
            'log1': 'The hello_world.start function is running',
            'log2': 'The bot sent the message "{msg}"'
        },
        'command': {
            'text1': 'Your location is city {city}.\n'
                     'Do you want to change the search city or are we looking by location?',
            'text1.1': 'Your location is city',
            'text2': 'In which city will we look for hotels?',
            'text3': 'Good choice, looking for a city {city} on the map',
            'text4': 'This is what I managed to find on the query - city {city}.\n'
                     'Press the button corresponding to your request',
            'text4.1': 'This is what I managed to find on the query - city',
            'text5': 'Select the date of entry',
            'text6': 'You have chosen the date of entry {res}',
            'text6.1': 'You have chosen the date of entry',
            'text7': 'Select the departure date',
            'text8': 'You have chosen the departure date  {res}',
            'text8.1': 'You have chosen the departure date ',
            'text9': 'The date of departure cannot coincide with the date of entry. '
                     'The minimum booking period of the hotel is 1 day. Please select the departure date again',
            'text10': 'So, how many hotels to choose?',
            'text11': 'Will photos be required for familiarization?',
            'text12': '{emoji1} Name of the hotel: <b>{hotel_name}</b>\n'
                      '{emoji2} Hotel website: <a>{web}</a>\n'
                      '{emoji3} Address: <code>{address}</code>\n'
                      '{emoji4} Open Yandex Maps: <a>{yamaps}</a>\n'
                      '{emoji5} Distance from the center: <code>{center}</code>\n'
                      '{emoji6} Price for the entire period: <code>{price}</code>\n'
                      '{emoji7} Date of entry: <code>{chk_in_date}</code>\n'
                      '{emoji8} Departure date: <code>{chk_out_date}</code>\n'
                      '{emoji9} Price per day: <code>{one_day_price}</code>\n'
                      '{emoji10} Rating: <code>{rating}</code>\n'
                      '{emoji11} Rating according to visitors: <code>{user_rating}</code>\n',
            'text13': 'Please indicate the acceptable range of prices for hotel accommodation separated by a space',
            'text14': 'Specify the acceptable range of distance in meters at which the hotel can be located '
                      'from the center separated by a space',
            'text15': 'You have selected a price range from {} rub to {} rub.',
            'text15.1': 'You have selected a price range from',
            'text16': 'You have selected the desired distance from the city center from {} meters to {} meters',
            'text16.1': 'You have selected the desired distance from the city center from',
            'text17': 'Nothing could be found for your query. Try changing the search parameters',
            'text18': 'Data entry error. The price range must be separated by a space',
            'text19': 'Data entry error. The distance range must be separated by a space'
        },
        'command_logging': {
            'log1': 'The command.start function with User location detection is started',
            'log2': 'The bot has determined the User`s location in the city "{city}"',
            'log3': 'The bot sent a message "{msg}"',
            'log4': 'The user clicked on the button "{button}" and chose the current location',
            'log5': 'The user clicked on the button "{button}" and preferred to choose another city to search for',
            'log6': 'city_choice function started',
            'log7': 'The bot sent a message "{msg}"',
            'log8': 'city_poisk function started',
            'log9': 'The bot sent a message "{msg2}", {cities}',
            'log10': 'The user has selected a search location "{button}"',
            'log11': 'city_choice_keyboard_callback function started',
            'log12': 'check_in_date_choice function started',
            'log13': 'chk_in_date_calendar function started',
            'log14': 'The user has chosen the date of entry {time_res}',
            'log15': 'chk_in_date_change function started',
            'log16': 'The user clicked on the button "{button}"',
            'log17': 'check_out_date_choice function started',
            'log18': 'chk_out_date_calendar function started',
            'log19': 'The user selected the departure date {time_res} the same as the entry date. '
                     'The bot has enabled an error notification',
            'log20': 'The user has selected the departure date {time_res}',
            'log21': 'chk_out_date_change function started',
            'log22': 'qty_hotels function started',
            'log23': 'city_poisk_keyboard_callback function started',
            'log24': 'hotels_poisk_in_the_city function started',
            'log25': 'hotels_poisk_keyboard_callback function started',
            'log26': 'hotels_info function started',
            'log27': 'The bot sent a message with information about the hotel',
            'log28': 'The bot sent a photo',
            'log29': 'photo_slide - the keyboard is open function started',
            'log30': 'price_range function started',
            'log31': 'The price_limiter function is running',
            'log32': 'The distance_range function is running',
            'log33': 'The distance_limiter function is running',
            'log34': 'The price_limiter_approve function is running',
            'log35': 'The price_limiter_approve function is running',
            'log36': 'Hotels are being searched on the {} page',
            'log37': 'The user entered the price range with an error',
            'log38': 'An error occurred in the price_limiter function {}',
            'log39': 'The user entered the distance range with an error',
            'log40': 'An error occurred in the distance_limiter function {}',
        },
        'command_acq': {
            'acq1': 'Accepted',
            'acq2': 'A search is being performed',
            'acq3': 'The answer is accepted',
        },
        'command_print_search_info': {
            'key1': 'ID hotel',
            'key2': 'Address',
            'key3': 'Coordinates',
            'key4': 'Distance from the center',
            'key5': 'Price for the entire period',
            'key6': 'Price for 1 day',
            'key7': 'Hotel rating',
            'key8': 'Rating according to visitors',
            'key9': 'Website'
        },
        'main_logging': {
            'log1': 'The bot is running'
        },
        'message_handlers_logging': {
            'log1': '/start command is running',
            'log2': '/hello_world command is running',
            'log3': '/lowprice command is running',
            'log4': '/highprice command is running',
            'log5': '/settings_func command is running',
            'log6': '/text command is running',
            'log7': '/history command is running',
            'log8': '/bestdeal command is running',
            
        },
        'requests_rapidapiHotels_logging': {
            'city_search': {
                'log1': 'The request to the server in the city_poisk function was successful',
                'log2': 'The response from the server in the city_search function exceeded the specified timeout',
                'log3': 'An error occurred in the city_poisk function {}'
            },
            'hotels_search_price': {
                'log1': 'The request to the server in the hotels_search_price function was successful',
                'log2': 'The response from the server in the hotels_search_price function exceeded the specified '
                        'timeout',
                'log3': 'An error occurred in the hotels_search_price function {}'
            },
            'photos_for_hotel': {
                'log1': 'The request to the server in the photos_for_hotel function was successful',
                'log2': 'The response from the server in the photos_for_hotel function exceeded the specified timeout',
                'log3': 'An error occurred in the photos_for_hotel function {}'
            }
        },
        'requests_rapidapiHotels': {
            'text1': 'Unfortunately, it was not possible to get information from the server. Please make a choice again'
        },
        'settings': {
            'text1': '{emoji} <b>Bot Menu</b>\n'
                     'This menu allows you to change the settings',
            'text01': 'This menu allows you to change the settings',
            'text2': '{emoji} <b>Bot Menu</b>\n'
                     'Select a language',
            'text02': 'Select a language',
            'text3': '{emoji} <b>Bot Menu</b>\n'
                     'Select a currency {emoji1}',
            'text03': 'Select a currency {emoji1}',
            
            'text4': 'Selected language - {lan}',
            'text5': 'Selected currency {cur}'
            
        },
        'settings_logging': {
            'log1': 'The settings.start function is started',
            'log2': 'The bot sent a message "{}"',
            'log3': 'The settings.change_settings function is started when switching from the main menu',
            'log4': 'The user clicked on the button "{}"',
            'log5': 'The settings.change_settings function is started when switching from the language selection menu',
            'log6': 'The settings.change_settings function is started when switching from the currency selection menu',
            'log7': 'The user clicked on the button "{}" and chose the appropriate language',
            'log8': 'The user clicked on the button "{}" and chose the appropriate currency',
            
        },
        'text': {
            'text1': 'And hello to you, my friend!',
            'text2': 'I don`t understand this yet'
        },
        'text_logging': {
            'log1': 'The user wrote "{}"',
            'log2': 'The bot replied "{}"'
        },
        'start': {
            'text1': 'Hello, {name} {emoji}!\n'
                     'I am a Bot from the travel agency Too Easy Travel!\n'
                     'I will help you choose a place for a vacation at great prices'
        },
        'start_logging': {
            'log1': 'The start.start function is started',
            'log2': 'The bot sent a message "{}"'
        },
        'history': {
            'text1': '<b>You sent the command {com}. '
                     'Date and time of sending the command {tm} {dt}</b>'
        },
        'history_logging': {
            'log1': 'The history.start function has been started',
            'log2': 'The bot sent a message "{}"',
            'log3': 'The bot forwarded the User`s message',
            
        },
        'sqlite': {
            'text1': 'An error has occurred. Please try again. '
                     'If the error persists, contact the Administrator'
        },
        'sqlite_logging': {
            'log1': 'The sqlite.data_add command is running',
            'log2': 'An error has occurred:\n{}',
            'log3': 'The sqlite.data_select command is running',
            'log4': 'An entry has been added to the database',
            'log5': 'A record/records was obtained from the database',
            
        },
    },
}

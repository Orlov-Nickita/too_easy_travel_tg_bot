f###### Версия бота 1.0:



## ОПИСАНИЕ БОТА

#### Данный бот разработан для турагенства Too Easy Travel и работает с сайтом Hotels.com.
#### Основная цель бота - помощь Пользователю в поиске отелей для планирования отдыха.
#### Бот на текущий момент умеет понимать несколько команд:
### 1. /lowprice
####
#### При выполнении данной команды Бот позволяет Пользователю найти самые выгодные (самые дешевые) отели в конкретном городе, который выбирает Пользователь. Последовательность выполнения команды заключается в определении города для поиска, определении планируемых дат для отдыха, в определении желаемого количества отелей для поиска (от 1 до 10) и в определении потребности Пользователя в предоставлении фотографии каждого из отелей. Бот, задавая наводящие вопросы, и Пользователь, отвечая на них, совместно создают определяющие поиск параметры. В результате чего Бот направляет в чат сообщения с информацией по найденным отелям и фотографии (если Пользователь этого пожелал).
####
#### Информация по отелю содержит следующие параграфы:
####
#### • Название отеля 
#### • Веб-сайт отеля
#### • Адрес
#### • Открыть Яндекс карты
#### • Удаленность от центра
#### • Цена за весь период
#### • Дата въезда
#### • Дата выезда
#### • Цена за сутки
#### • Рейтинг
#### • Рейтинг по мнению посетителей
####
### 2. /highprice (команда аналогична /lowprice с отличием лишь в сортировке)
#### При выполнении данной команды Бот позволяет Пользователю найти самые дорогие отели в конкретном городе, который выбирает Пользователь. Последовательность выполнения команды заключается в определении города для поиска, определении планируемых дат для отдыха, в определении желаемого количества отелей для поиска (от 1 до 10) и в определении потребности Пользователя в предоставлении фотографии каждого из отелей. Бот, задавая наводящие вопросы, и Пользователь, отвечая на них, совместно создают определяющие поиск параметры. В результате чего Бот направляет в чат сообщения с информацией по найденным отелям и фотографии (если Пользователь этого пожелал). 
####
#### Информация по отелю содержит следующие параграфы:
####
#### • Название отеля
#### • Веб-сайт отеля
#### • Адрес
#### • Открыть Яндекс карты
#### • Удаленность от центра
#### • Цена за весь период
#### • Дата въезда
#### • Дата выезда
#### • Цена за сутки
#### • Рейтинг
#### • Рейтинг по мнению посетителей
####
### 3. /bestdeal
#### При выполнении данной команды Бот позволяет Пользователю найти самые отели в конкретном городе, который выбирает Пользователь, на определенном удалении от центра города и в определенном диапозоне цен. Последовательность выполнения команды заключается в определении города для поиска, определении планируемых дат для отдыха, в определении диапозона расстояния на котором может располагаться искомый отель, в определении диапозона цен, в рамках которых может стоить проживание в искомом отеле, в определении желаемого количества отелей для поиска (от 1 до 10) и в определении потребности Пользователя в предоставлении фотографии каждого из отелей. Бот, задавая наводящие вопросы, и Пользователь, отвечая на них, совместно создают определяющие поиск параметры. В результате чего Бот направляет в чат сообщения с информацией по найденным отелям и фотографии (если Пользователь этого пожелал). 
#### 
#### Информация по отелю содержит следующие параграфы:
####
#### • Название отеля
#### • Веб-сайт отеля
#### • Адрес
#### • Открыть Яндекс карты
#### • Удаленность от центра
#### • Цена за весь период
#### • Дата въезда
#### • Дата выезда
#### • Цена за сутки
#### • Рейтинг
#### • Рейтинг по мнению посетителей
####
#### Также Бот имеет служебные команды, которые позволяют Пользователю взаимодействовать непосредственно с самим Ботом, например, поменять язык или валюту:
### 1. /history
#### Данная команда позволяет Пользователю получить хронолгическую сводку отправленных команд и полученных ответов от Бота: информация о найденных отелях и фотографии
####
### 2. /settings
#### Данная команда позволяет Пользователю сменить языка интерфейса на Английский или на Русский, сменить валюту на Доллар, Евро, Рубль
####
## АРХИТЕКТУРА БОТА
####
#### Бот устроен следующим образом:
#### В корневой папке располагаются файлы
#### - .env: Файл, в котором хранятся переменные окружения. Это файл, который содержится в gitignore и хранит в себе необходимые для работы Бота секретные данные
#### - .env.template: Файл, в который является примером заполнения файла .env
#### - .gitignore: Файл, который содержит информацию, которая не должна быть размещена в Git репозитории
#### - loader.py: В этом файле описывается класс Пользователь для хранения поисковой информации, подгружаются переменные окружения для корректной работы Бота
#### - main.py: Основной запускаемый файл Бота
#### - message_handlers.py: Файл, в котором описываются все известные Боту команды и сценарий их работы
#### - readme.txt: Файл, который Вы сейчас читаете
#### - requirements.txt: Файл, который хранит перечень всех библиотек, которые были задействованы в написании Бота
#### - user_database.db: База данных Пользователей. Для ее понятного представления предлагается использование программы DB Browser (SQLite)
#### - Папка commands_and_keyboards: Данная папка содержит все команды Бота и файл со всеми описываемыми клавиатурами Бота
#### - Папка logs: Данная папка содержит файл - журнал событий - логгер, в который записываются все события в процессе работы Бота. Начиная от взаимодействия Пользователя с Ботом, заканчивая всеми ошибками, которые возникают в работе Бота
#### - Папка useful_add_func: Данная папка содержит дополнительные полезные функции для облегчения работы Бота. Также содержит файл, который содержит в себе функции работы с сайтом Hotels.com и файл, в котором определяется класс Фотоальбом
#### - Папка utils: Данная папка содержит в себе словарь с заранее подготовленными языковыми ответами, логгер (журнал событий), файл работы с SQLite БД
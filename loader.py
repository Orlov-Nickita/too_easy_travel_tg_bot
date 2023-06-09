import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('Bot_token'))
rapidkey = os.getenv("rapidapi-key")
rapidhost = os.getenv("rapidapi-host")


class User_search:
    users = dict()
    """
    Класс, необходимый для хранения поисковой информации
    Attributes:
        sort (str): Содержится параметр сортировки отелей
        lang (str): Содержится аббревиатура выбранного языка интерфейса Бота. По умолчанию - Русский
        locale (str): Условное обозначение кода языка для получения информации с сервера в правильном языковом формате
        currency (str): Содержится информация выбранной валюты. По умолчанию - Рубль
        page_number (int): Номер страницы с которой ведется поиск отелей
        min_price (int): Содержится минимальная стоимость проживания в отеле
        max_price (int): Содержится максимальная стоимость проживания в отеле
        min_dist (int): Минимально желаемое расстояние отеля от центра города
        max_dist (int): Максимально желаемое расстояние отеля от центра города
        city (str): Содержится название города, в котором осуществляется поиск.
        found_cities (dict): Содержится информация обо всех найденных городах похожих по названию к искомому.
        city_id (int): Содержится идентификационный номер id, необходимый для поиска информации по сайту hotels.com,
        так как поиск отелей в городе осуществляется не по названию города, а по его id номеру.
        hotels_qty (dict): Для заданного количества отелей находится заранее определенная информация и упаковывается
        в словарь из словарей, который имеет следующий шаблон:
        {'Название отеля': {Информация по отелю}, 'Название отеля': {Информация по отелю}}
        Информация по отелю содержит в себе ID отеля, адрес, координаты, удаленность от центра, цену за 1 сутки, рейтинг
        отеля по мнению сайта, рейтинг отеля с точки зрения посетителей, ссылку на сайт.
        photos_dict (dict): Содержится словарь {'ID отеля': [список ссылок на фотографии]}, в последствии превращаемый
        в итерируемый объект путем создания объекта класс Photo_album
        photos_dict_urls (dict): Содержится словарь {'message.id': [итерируемый в обе стороны список фотографий]},
        который привязывается уже не к id отеля, а к id самого сообщения. Так как message_id для сообщения с
        фотографией и с клавиатурой одинаковые, этот словарь позволяет программе понимать из какого словаря выбирать
        фотографии в зависимости от нажатой клавиши под соответствующей фотографией
        check_in (str): Содержится дата въезда Пользователя
        check_out (str): Содержится дата выезда Пользователя
        rest_days (int): Содержится количество дней отдыха в отеле
    """
    
    def __init__(self):
        self.sort = None
        self.lang = 'ru'
        self.locale = 'ru_RU'
        self.currency = 'RUB'
        self.pagenumber = 1
        self.min_price = None
        self.max_price = None
        self.min_dist = None
        self.max_dist = None
        self.location = None
        self.city = None
        self.hotels_qty = None
        self.found_cities = None
        self.city_id = None
        self.hotels = None
        self.photos_dict = None
        self.photos_dict_urls = None
        self.check_in = None
        self.check_out = None
        self.rest_days = None
    
    def get_user(self, user_id):
        """
        Метод, который при отсутствии в словаре текущего пользователя добавляет пользователя в словарь, а затем
        возвращает информацию по текущему пользователю
        """
        if user_id not in self.users:
            User_search.add_user(self, user_id)
        
        return User_search.users[user_id]
    
    @classmethod
    def add_user(cls, user, user_id):
        """
        Метод, для добавления пользователя в словарь пользователей
        """
        cls.users[user_id] = user

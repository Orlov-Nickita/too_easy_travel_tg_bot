import json
from urllib.request import urlopen
from googletrans import Translator
from my_bot.loader import search

translator = Translator()

def ip_search() -> str:
    """
    Функция, которая определяет местоположение Пользователя через ip-адрес
    :return: Возвращается название города, в котором находится сейчас Пользователь
    :rtype: str
    """
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = translator.translate(data['city'], dest=search.lang).text

    return city

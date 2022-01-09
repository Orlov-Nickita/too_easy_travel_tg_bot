import json
from typing import Dict
import telebot
import requests
from loader import rapidkey, rapidhost, bot
import datetime


def city_search(message: telebot.types.Message, city_name: str) -> None or Dict:
    """
    Функция для поиска на сайте Hotels.com всех подходящих наименований городов по введенному наименованию
    Пользователем.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param city_name: В качестве параметра передается введенный (или выбранный найденный по ip-адресу) город
    места нахождения
    :type city_name: str
    :return: Если код ответа сервера 200, тогда возвращается словарь с информацией городов с сайта Hotels.com, если код
    ответа иной в чат отправляется сообщение о том, что сервер недоступен.
    :rtype: Dict
    """
    try:
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": city_name, "locale": "ru_RU", "currency": "RUB"}
        headers = {
            'x-rapidapi-host': rapidhost,
            'x-rapidapi-key': rapidkey
            }
        cities = requests.request(method = "GET", url = url, headers = headers, params = querystring,
                                  timeout = 10
                                  ).json()
        # with open('cities.json', 'w', encoding = 'utf-8') as file:
        #     json.dump(cities, file, indent = 4, ensure_ascii = False)
    except requests.Timeout:
        bot.send_message(chat_id = message.chat.id, text = 'К сожалению, сервер сейчас недоступен. Попробуйте, '
                                                           'пожалуйста, еще раз')
    else:
        return cities


def hotels_search_lowprice(message: telebot.types.Message, city_destination_id: int) -> None or Dict:
    """
    Функция для нахождения самых дешевых отелей в выбранном городе
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param city_destination_id: В качестве параметра передается id выбранного города для осуществления поиска отелей
    :type city_destination_id: int
    :return: Если код ответа сервера 200, тогда возвращается словарь с информацией отелей с сайта Hotels.com, если код
    ответа иной в чат отправляется сообщение о том, что сервер недоступен.
    :rtype: Dict
    """
    try:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days = 1)
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": city_destination_id, "checkIn": today, "checkOut": tomorrow,
                       "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}
        headers = {
            'x-rapidapi-host': rapidhost,
            'x-rapidapi-key': rapidkey
            }
        hotels = requests.request(method = "GET", url = url, headers = headers, params = querystring,
                                  timeout = 10
                                  ).json()
        # with open('hotels_in_city.json', 'w', encoding = 'utf-8') as file:
        #     json.dump(hotels, file, indent = 4, ensure_ascii = False)
    except requests.Timeout:
        bot.send_message(chat_id = message.chat.id, text = 'К сожалению, сервер сейчас недоступен. Попробуйте, '
                                                           'пожалуйста, еще раз')
    else:
        return hotels


def photos_for_hotel(message: telebot.types.Message, hotel_id: int) -> None or Dict:
    """
    Функция для нахождения фотографий найденных отелей в выбранном городе.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param hotel_id: В качестве параметра передается id отеля для поиска фотографий для этого отеля.
    :type hotel_id: int
    :return: Если код ответа сервера 200, тогда возвращается словарь с фотографиями с сайта Hotels.com, если код
    ответа иной в чат отправляется сообщение о том, что сервер недоступен.
    :rtype: Dict
    """
    try:
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": hotel_id}
        headers = {
            'x-rapidapi-host': rapidhost,
            'x-rapidapi-key': rapidkey
            }
        photos = requests.request(method = "GET", url = url, headers = headers, params = querystring,
                                  timeout = 10
                                  ).json()
        # with open('photos.json', 'w', encoding = 'utf-8') as file:
        #     json.dump(photos, file, indent = 4, ensure_ascii = False)
    except requests.Timeout:
        bot.send_message(chat_id = message.chat.id, text = 'К сожалению, сервер сейчас недоступен. Попробуйте, '
                                                           'пожалуйста, еще раз')
    else:
        return photos

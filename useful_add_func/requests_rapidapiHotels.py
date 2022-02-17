# import json
from typing import Dict
import telebot
import requests
from loader import rapidkey, rapidhost, bot, search
import logging

from utils.languages_for_bot import lang_dict

headers = {
    'x-rapidapi-host': rapidhost,
    'x-rapidapi-key': rapidkey
}


def city_search(message: telebot.types.Message, locale: str, city_name: str, currency: str) -> None or Dict:
    """
    Функция для поиска на сайте Hotels.com всех подходящих наименований городов по введенному наименованию
    Пользователем.
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param locale: Код языка для получения информации с сервера в нужном языковом формате
    :type locale: str
    :param city_name: В качестве параметра передается введенный (или выбранный найденный по ip-адресу) город
    места нахождения
    :type city_name: str
    :param currency: Валюта
    :type currency: str
    :return: Если код ответа сервера 200, тогда возвращается словарь с информацией городов с сайта Hotels.com, если код
    ответа иной в чат отправляется сообщение о том, что сервер недоступен.
    :rtype: Dict
    """
    try:
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": city_name, "locale": locale, "currency": currency}
        
        cities = requests.request(method="GET", url=url, headers=headers, params=querystring,
                                  timeout=20
                                  ).json()
        # with open('cities.json', 'w', encoding='utf-8') as file:
        # json.dump(cities, file, indent=4, ensure_ascii=False)
        logging.info(lang_dict[search.lang]['requests_rapidapiHotels_logging']['city_search']['log1'], extra=search.user_id)
    except requests.Timeout:
        bot.send_message(chat_id=message.chat.id, text=lang_dict[search.lang]['requests_rapidapiHotels']['text1'])
        logging.warning(lang_dict[search.lang]['requests_rapidapiHotels_logging']['city_search']['log2'], extra=search.user_id)
    except Exception as Ex:
        logging.exception(lang_dict[search.lang]['requests_rapidapiHotels_logging']['city_search']['log3'].format(Ex), extra=search.user_id)
    
    else:
        return cities


def hotels_search_price(message: telebot.types.Message, city_destination_id: int, pagenumber: int, chk_in: str,
                        chk_out: str, sort: str, locale: str, currency: str, min_price: int = None,
                        max_price: int = None) -> None or Dict:
    """
    Функция для нахождения самых дешевых отелей в выбранном городе
    :param message: В качестве параметра передается сообщение из чата
    :type message: telebot.types.Message
    :param city_destination_id: В качестве параметра передается id выбранного города для осуществления поиска отелей
    :type city_destination_id: int
    :param pagenumber: Номер страницы поиска отелей
    :type pagenumber: int
    :param chk_in: В качестве параметра передается желаемая дата въезда Пользователя
    :type chk_in: str
    :param chk_out: В качестве параметра передается желаемая дата выезда Пользователя
    :type chk_out: str
    :param min_price: Минимальная стоимость проживания в отеле
    :type min_price: int
    :param max_price: Максимальная стоимость проживания в отеле
    :type max_price: int
    :param sort: В качестве параметра передается тип сортировки
    :type sort: str
    :param locale: Код языка для получения информации с сервера в нужном языковом формате
    :type locale: str
    :param currency: Валюта
    :type currency: str
    :return: Если код ответа сервера 200, тогда возвращается словарь с информацией отелей с сайта Hotels.com, если код
    ответа иной в чат отправляется сообщение о том, что сервер недоступен.
    :rtype: Dict
    """
    try:
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": city_destination_id, "pageNumber": pagenumber, "pageSize": 25,
                       "checkIn": chk_in, "checkOut": chk_out, "priceMin": min_price, "priceMax": max_price,
                       "sortOrder": sort, "locale": locale, "currency": currency}
        
        hotels = requests.request(method="GET", url=url, headers=headers, params=querystring,
                                  timeout=20
                                  ).json()
        # with open('hotels_in_city.json', 'w', encoding='utf-8') as file:
        #     json.dump(hotels, file, indent=4, ensure_ascii=False)
        logging.info(lang_dict[search.lang]['requests_rapidapiHotels_logging']['hotels_search_price']['log1'], extra=search.user_id)
    
    except requests.Timeout:
        bot.send_message(chat_id=message.chat.id, text=lang_dict[search.lang]['requests_rapidapiHotels']['text1'])
        logging.warning(lang_dict[search.lang]['requests_rapidapiHotels_logging']['hotels_search_price']['log2'], extra=search.user_id)
    except Exception as Ex:
        logging.exception(
            lang_dict[search.lang]['requests_rapidapiHotels_logging']['hotels_search_price']['log3'].format(Ex), extra=search.user_id)
    
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
        photos = requests.request(method="GET", url=url, headers=headers, params=querystring,
                                  timeout=20
                                  ).json()
        # with open('photos.json', 'w', encoding='utf-8') as file:
        #     json.dump(photos, file, indent=4, ensure_ascii=False)
        logging.info(lang_dict[search.lang]['requests_rapidapiHotels_logging']['photos_for_hotel']['log1'], extra=search.user_id)
    
    except requests.Timeout:
        bot.send_message(chat_id=message.chat.id, text=lang_dict[search.lang]['requests_rapidapiHotels']['text1'])
        logging.warning(lang_dict[search.lang]['requests_rapidapiHotels_logging']['photos_for_hotel']['log2'], extra=search.user_id)
    except Exception as Ex:
        logging.exception(
            lang_dict[search.lang]['requests_rapidapiHotels_logging']['photos_for_hotel']['log3'].format(Ex), extra=search.user_id)
    
    else:
        return photos

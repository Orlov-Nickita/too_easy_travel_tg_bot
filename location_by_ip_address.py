import json
from urllib.request import urlopen
from googletrans import Translator

def ip_search():
    
    translator = Translator()
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    
    city = translator.translate(data['city'], dest = 'ru')
    
    return city.text

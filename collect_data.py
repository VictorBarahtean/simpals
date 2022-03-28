import requests
import time
import json
import lxml
from bs4 import BeautifulSoup

url_init = 'https://partners-api.999.md/adverts'
current_currency = {}

# get adverts from server API
def get_adverts(url):
    return requests.get(url, auth=('apuUo-UF6yhfoNVVTKWrb5Z8ecru', '')).json()

# get advert from server API
def get_advert(url, id_advert):
    return requests.get(f"{url}/{id_advert}", auth=('apuUo-UF6yhfoNVVTKWrb5Z8ecru', '')).json()

# we need to download each advert separately
def create_sorted_adverts(adverts, url):
    # I tried this method but is not working because we need time to send request to server
    #return dict({advert['id']:get_advert(url, advert['id']) for advert in adverts['adverts']})

    result = []
    for advert in adverts['adverts']:
        result.append({'_id':advert['id'], 'advert':get_advert(url, advert['id'])})
        time.sleep(1)
    
    return result

# save all advert to file json
def save_adverts_to_json(adverts):
    with open("all_adverts.json", "w", encoding="utf-8") as file:
        json.dump({'adverts':adverts}, file, ensure_ascii=False)

# collect currencies from bnm.md and decode with BeatifulSoup
def collect_current_currencies():
    global current_currency

    req = requests.get("https://www.bnm.md/")
    soup = BeautifulSoup(req.text, 'lxml')

    for unit in soup.find(class_='view-rates').find_all('li'):
        current_currency[unit.find(class_='currency').text] = unit.find(class_='rate').text

    with open("current_currency.json", "w", encoding="utf-8") as file:
        json.dump(current_currency, file, ensure_ascii=False)
    
    return current_currency
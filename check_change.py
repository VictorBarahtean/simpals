from os.path import exists
import json
from collect_data import create_sorted_adverts, get_adverts, collect_current_currencies
from connector import insert_advert, update_advert, delete_advert, get_adverts_all

# check if old adverts is different from API
def check_adverts_changes(url):
    # get all adverts from API
    json_new = get_adverts(url)
    # get all adverts from API with detail
    adverts_new = create_sorted_adverts(json_new, url)
    # collect current currencies
    collect_current_currencies()
    # flag for check if we are downloading from MongoDB
    online = False
    
    if exists("all_adverts.json"):
        with open("all_adverts.json", encoding="utf-8") as file:
            adverts_old = json.load(file)
    else:
        adverts_old = get_adverts_all()
        online = True
    
    if len(adverts_old) == 0:
       adverts_old = {'adverts':{'_id': 0 }}
       online = False

    if len(adverts_new) == 0:
       adverts_new = {'adverts':{'_id': 0 }}  
        
    # check if is the difference between new and old adverts
    if sorted({'adverts':adverts_new}.items()) != sorted({'adverts':adverts_old}.items()):
        # sorted adverts with "_id"
        adverts_new_sorted = sorted(adverts_new, key=lambda d:d['_id'])
        adverts_old_sorted = sorted(adverts_old, key=lambda d:d['_id'])

        i = 0
        j = 0

        while(i < len(adverts_new_sorted) and j < len(adverts_old_sorted)):
            # check if is the difference between new and old advert
            if adverts_old_sorted[j]['_id'] == adverts_new_sorted[i]['_id']:

                if sorted(adverts_old_sorted[j].items()) != sorted(adverts_new_sorted[i].items()):
                    # update advert
                    update_advert(adverts_new_sorted[i], adverts_old_sorted[j])

                i += 1
                j += 1
            elif adverts_old_sorted[j]['_id'] > adverts_new_sorted[i]['_id']:
                # insert new advert
                insert_advert(adverts_new_sorted[i])
                i += 1
            
            elif adverts_old_sorted[j]['_id'] < adverts_new_sorted[i]['_id']:
                # delete old advert
                delete_advert(adverts_old_sorted[j])
                j += 1
        
        with open("all_adverts.json", "w", encoding="utf-8") as file:
            json.dump(adverts_new_sorted, file, ensure_ascii=False)

    elif online:
        with open("all_adverts.json", "w", encoding="utf-8") as file:
            json.dump(adverts_new, file, ensure_ascii=False)
    
    return adverts_new
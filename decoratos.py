from collect_data import collect_current_currencies, current_currency

def convert_currency(func):
    if len(current_currency) == 0:
        collect_current_currencies()
        
    def convert(*args, **kwargs):
        adverts = list(args)[0]
        is_list = isinstance(adverts, list)
        adverts = adverts if is_list else [adverts]

        i = 0
        for advert in adverts:
            if advert['advert']['price']['unit'] == 'eur':
                j = 0
                for currencies in advert['advert']['price']['currencies']:  
                    if currencies['unit'] == 'mdl':
                        adverts[i]['advert']['price']['currencies'][j]['value'] = round(float(current_currency['EUR']) * float(advert['advert']['price']['value']))
                    j += 1
            
            i += 1

        args = list(args)
        args[0] = adverts if is_list else adverts[0] 
        args = tuple(args)    

        func(*args, **kwargs)
    return convert
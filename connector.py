from pymongo import MongoClient, errors
from decoratos import convert_currency

# conection to MongoDB
cluster = MongoClient("mongodb+srv://kabbban:Admin.2019@cluster0.bobzi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Simpals"]
collection = db["adverts"]

@convert_currency
def insert_adverts(adverts):
    # insert adverts to MongoDB
    try:
        collection.insert_many(adverts)
    except errors.BulkWriteError:
        collection.delete_many({})
        collection.insert_many(adverts)

@convert_currency
def insert_advert(advert):
    # insert advert to MongoDB
    collection.insert_one(advert)

@convert_currency
def update_advert(new_advert, old_advert):
    # update advert to MongoDB
    collection.update_one({"advert" : old_advert['advert']}, {"$set":{"advert" : new_advert['advert']}})

def delete_advert(advert):
    # delete advert from MongoDB
    collection.delete_one({'_id':advert['_id']})

def get_adverts_all():
    # get all adverts from MongoDB
    return list(collection.find())

def delete_adverts():
    # detele all adverts from MongoDB
    collection.delete_many({})
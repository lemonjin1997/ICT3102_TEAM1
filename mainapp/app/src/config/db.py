from pymongo import MongoClient
conn = MongoClient("mongodb://lemonjin:pangjinxiang@database:27017")

async def get_db():
    db = conn["mydatabase"]
    return db

async def get_col_beacon(db):
    collectionBeacon = db["Beacon"]
    return collectionBeacon
async def get_col_user(db):
    collectionUser = db["User"]
    return collectionUser
async def get_col_ping(db):
    collectionPing = db["Ping"]
    return collectionPing


# TODO upload beacon data into db and cache it as dic

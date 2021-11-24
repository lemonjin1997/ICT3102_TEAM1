from pymongo import MongoClient


conn = MongoClient("mongodb://lemonjin:pangjinxiang@database:27017")
def get_db():
    db = conn["mydatabase"]
    if db.get_collection("Beacon") is None: 
        db.create_collection('Beacon')
    if db.get_collection("User") is None: 
        db.create_collection('User')
    if db.get_collection("Ping") is None: 
        db.create_collection('Ping')
    return db

def get_col_beacon(db):
    collectionBeacon = db.get_collection("Beacon")
    return collectionBeacon
def get_col_user(db):
    collectionUser = db.get_collection("User")
    return collectionUser
def get_col_ping(db):
    collectionPing = db.get_collection("Ping")
    return collectionPing


# TODO upload beacon data into db and cache it as dic

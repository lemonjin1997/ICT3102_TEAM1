from fastapi import APIRouter

from src.models.user import User, Beacon, Ping
from src.config.db import collectionBeacon, collectionUser, collectionPing ,db
from src.schemas.user import *
import datetime

user = APIRouter()

# todo for cache find the timeout dic
cache = dict() 


@user.get('/')
async def find_all_users():

    
    #print collection in database
    print(db.list_collection_names())

    #print samples
    collectionBeacon = db["Beacon"]
    collectionUser = db["User"]
    collectionPing = db["Ping"]
    for x in collectionPing.find():
        print(x)
    for x in collectionUser.find():
        print(x)
    for x in collectionBeacon.find():
        print(x)
    return ""

@user.post('/ping_server')
async def ping_server(ping: Ping):
    ping.time_stamp = str(datetime.now())
    print(dict(ping))
    beacon = collectionBeacon.find_one({"beacon_mac": ping.beacon_mac})
    user = collectionUser.find_one({"name": ping.name})
    print(beacon)
    print(user)
    if user is None:
        collectionUser.insert_one({"name": ping.name})
    if beacon is not None:
        collectionPing.insert_one(dict(ping))

    print(db["User"].find()[0])
    print(db["Beacon"].find()[0])
    return ""

@user.get('/beacon')
async def find_all_beacon():
    # definiation of online is sent a ping in the last ten minutes.
    
    online_beacon = db["Ping"].find(
        {"time_stamp": { 
            "$gt": "",  
            "$lt": ""
            }} )
    for x in online_beacon:
        print(x)
    

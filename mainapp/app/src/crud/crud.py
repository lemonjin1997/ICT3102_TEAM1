from models.user import *
from config.db import *
import time

def extract_beacon(collectionPing, start_time, end_time, staff_id, tmp_dic):
    pings = collectionPing.find(
        {
            "$and": 
            [
            {
                "time_stamp": 
                { 
                    "$gt": str(start_time),"$lt": str(end_time)
                }
            }
            ,
            {
                "name": str(staff_id)
            }
            ]
            
        }
    )
    pingtotal = collectionPing.find()
    ping_dic = {}
    tmp_list = []
    for x in pings:
        beacon_mac = tmp_dic[x['beacon_mac']]
        tmp_list.append({
            "level":beacon_mac['level'],
            "location":beacon_mac['location'],
            "timestamp":x['time_stamp']
        })
    ping_dic['location'] = tmp_list
    return ping_dic

def insert_ping(name, beacon_mac):
    db = get_db()
    time_stamp = int(time.time())
    ping = Ping(name=name, beacon_mac=beacon_mac, time_stamp=time_stamp)
    
    # check beacon exist
    collectionBeacon = get_col_beacon(db)
    collectionPing = get_col_ping(db)
    collectionUser = get_col_user(db)
    beacon = collectionBeacon.find_one({"beacon_mac": ping.beacon_mac})
    user = collectionUser.find_one({"name" : ping.name})
    # print("beacon:", beacon)
    # print("user", user)
    if user is None:
        collectionUser.insert_one({"name": ping.name})
    if beacon is not None:
        collectionPing.insert_one(dict(ping))
        return dict(ping)
    else:
        print("error beacon not found")
    
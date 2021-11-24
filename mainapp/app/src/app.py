from flask import Flask
from flask import request
from config.db import *
from schemas.user import *
from models.user import *
import time


app = Flask(__name__)

db = get_db()
# cache  = {}
tmp_dic = {}

def readBeacons():
    file = open('src/BeaconLocation.txt')
    #print(list(file))
    insert_list = []
    for x in list(file):
        x = x.replace('"', '')
        x = x.replace("\n", '')
        x = x.replace("'", '')
        x = x.replace(' ', "")
        tmp_detail = x.split(':')
        print(tmp_detail)
        tmp_dic[tmp_detail[0]] = {"location" : tmp_detail[1] , "level" :  tmp_detail[2]}
        insert_list.append({"beacon_mac": tmp_detail[0] , "location" : tmp_detail[1] , "level" :  tmp_detail[2]})
    
    get_col_beacon(db).insert_many(insert_list)

@app.route('/', methods = ['GET'])
def dashboard():
    #print collection in database
    print(db.list_collection_names())

    #print samples
    collectionBeacon = get_col_beacon(db)
    collectionPing = get_col_ping(db)
    collectionUser = get_col_user(db)
    for x in collectionPing.find():
        print(x)
    for x in collectionUser.find():
        print(x)
    for x in collectionBeacon.find():
        print(x)
    return str(db.list_collection_names())


@app.route('/ping_server', methods = ['GET'])
def ping_server():
    db = get_db()
    # Populate data
    name = request.args.get('name')
    beacon_mac = request.args.get('beacon_mac')
    print(name)
    print(beacon_mac)
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
    collectionPing.insert_one(dict(ping))
    
    collectionBeacon = get_col_beacon(db)
    collectionPing = get_col_ping(db)
    collectionUser = get_col_user(db)
    beacon = collectionBeacon.find_one({"beacon_mac": ping.beacon_mac})
    user = collectionUser.find_one({"name" : ping.name})
    ping = collectionPing.find_one({"beacon_mac": ping.beacon_mac})
    # print("beacon:2", beacon)
    # print("user:2", user)
    # print("ping:2", ping)

    return beacon_mac+name+str(time_stamp)

@app.route('/ping_HACWS', methods = ['GET'])
def ping_HACWS():
    db = get_db()
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    start_time = int(time.time() - 3600)
    end_time = int(time.time())
    print("start_time", start_time)
    print("end_time", end_time)
    collectionPing = get_col_ping(db)
    pings = collectionPing.find(
        {"time_stamp": { 
            "$gt": str(start_time),"$lt": str(end_time)
            }}
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

if __name__== "__main__":
    readBeacons()
    print(tmp_dic)
    app.run(debug=True, host='0.0.0.0', port=5000)
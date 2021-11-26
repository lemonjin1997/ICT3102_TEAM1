from flask import Flask, render_template
from flask import request
from config.db import *
from schemas.user import *
from models.user import *
from crud.crud import *
import time
from expiringdict import ExpiringDict


app = Flask(__name__, template_folder='template')

db = get_db()
# cache  = {}
tmp_dic = {}
timeout_dic = ExpiringDict(max_age_seconds=3600, max_len=1000)

def readBeacons():
    file = open('src/BeaconLocation.txt')
    #print(list(file))
    insert_list = []
    for x in list(file):
        x = x.replace("\n", '')
        tmp_detail = x.split(':')
        print(tmp_detail)
        tmp_dic[tmp_detail[0]] = {"location" : tmp_detail[1] , "level" :  tmp_detail[2]}
        insert_list.append({"beacon_mac": tmp_detail[0] , "location" : tmp_detail[1] , "level" :  tmp_detail[2]})
    
    get_col_beacon(db).insert_many(insert_list)

@app.route('/', methods = ['GET'])
def dashboard():
    dashboard_dic = tmp_dic
    # for x in dashboard_dic.keys():
    #     if dict(timeout_dic).get(x) is not None:
    #         dashboard_dic[x]['count'] = len(dict(timeout_dic).get(x))
    #     else:
    #         dashboard_dic[x]['count'] = 0
    # for x in dict(timeout_dic).keys():
    #     tmp_list.extend(dict(timeout_dic)[x])
    return render_template('dashboard.html', beacons=dashboard_dic, timeout_dic=dict(timeout_dic))


@app.route('/ping_server', methods = ['POST'])
def ping_server():
    # Populate data
    staff_id = request.json['staff_id']
    beacon_mac = request.json['mac']
    rssi = request.json['rssi']
    ping = insert_ping(staff_id, beacon_mac, rssi)
    
    if timeout_dic.get(ping['time_stamp']) is None:
        timeout_dic[ping['time_stamp']] = ping

    print(beacon_mac+staff_id+rssi)
        
    return beacon_mac+staff_id+rssi

@app.route('/extractbeacon', methods = ['GET'])
def ping_HACWS():
    db = get_db()
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    staff_id = request.args.get('staff_id')
    input = str(start_time) + str(end_time) + staff_id
    collectionPing = get_col_ping(db)
    ping_dic = extract_beacon(collectionPing, start_time, end_time, staff_id, tmp_dic)
    
    return input + str(ping_dic)

if __name__== "__main__":
    if get_col_beacon(get_db()).count() <= 0:
        readBeacons()
    print(tmp_dic)
    app.run(debug=True, host='0.0.0.0', port=5000)
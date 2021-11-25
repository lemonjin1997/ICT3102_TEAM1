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
    for x in dashboard_dic.keys():
        if dict(timeout_dic).get(x) is not None:
            dashboard_dic[x]['count'] = len(dict(timeout_dic).get(x))
        else:
            dashboard_dic[x]['count'] = 0
    tmp_list = []
    for x in dict(timeout_dic).keys():
        tmp_list.extend(dict(timeout_dic)[x])

    return render_template('dashboard.html', beacons=dashboard_dic, timeout_list=tmp_list)


@app.route('/ping_server', methods = ['GET'])
def ping_server():
    # Populate data
    name = request.args.get('name')
    beacon_mac = request.args.get('beacon_mac')
    ping = insert_ping(name, beacon_mac)
    
    if timeout_dic.get(beacon_mac) is None:
        timeout_dic[beacon_mac] = [ping]
    else:
        timeout_dic[beacon_mac].append(ping)
    return beacon_mac+name

@app.route('/ping_HACWS', methods = ['GET'])
def ping_HACWS():
    db = get_db()
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    staff_id = request.args.get('staff_id')
    staff_id = "lemonjin"
    start_time = int(time.time() - 3600)
    end_time = int(time.time())
    input = str(start_time) + str(end_time) + staff_id
    collectionPing = get_col_ping(db)
    ping_dic = extract_beacon(collectionPing, start_time, end_time, staff_id, tmp_dic)
    
    return input + str(ping_dic)

if __name__== "__main__":
    readBeacons()
    print(tmp_dic)
    app.run(debug=True, host='0.0.0.0', port=5000)
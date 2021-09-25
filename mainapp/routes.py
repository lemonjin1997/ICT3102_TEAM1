from flask import jsonify, request, render_template, url_for, redirect
from mainapp import *
from mainapp.utilities import * 
import time

@application.route('/', methods=['GET'])
@application.route('/home/', methods=['GET'])
async def home():
    introStr = "This flask server for ICT3102: " + "\n" + "/add device : to add device"
    return introStr

@application.route('/list_device', methods=['GET'])
async def listDevice():
    return jsonify(deviceDic)

@application.route('/temp_route', methods=['POST'])
def temp_route():
    staff_id = request.json['staff_id']
    beacon_mac = request.json['mac']
    return {'response' : f'Successfully received payload (ID:{staff_id} MAC:{beacon_mac})'}

@application.route('/device_ping', methods=['POST'])
async def devicePing():
    staff_id = request.args.get('staff_id', type = int)
    location = request.args.get('location', type = str)
    level = request.args.get('level', type = int)
    cur = con.cursor()
    cur.execute("SELECT * FROM staff WHERE staff_id=?", (staff_id,))
    db_staff_id = cur.fetchall()
    print(db_staff_id)
    if len(db_staff_id) == 0:
        cur.execute("INSERT INTO staff(staff_id) VALUES (?)", (staff_id,))
        con.commit()
    
    tmpDic = {"level" : level, "location" : location , "timestamp" : int(time.time())}
    insertLocation(con, tmpDic, staff_id)
    if staff_id in deviceDic.keys():
        deviceDic[staff_id].append(tmpDic)
        return "Device updated."
    else:
        deviceDic[staff_id] = [tmpDic]
        return "Device added."

@application.route('/extractbeacon', methods=['GET'])
async def extractbeacon():
    staff_id = request.args.get('staff_id', type = int)
    start_time = request.args.get('start_time', type = int)
    end_time = request.args.get('end_time', type = int)
    
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT * FROM location WHERE staff_id = ? AND timestamp>? AND timestamp < ? ", (staff_id, start_time, end_time, ))
    location = cur.fetchall()
    return jsonify(location)


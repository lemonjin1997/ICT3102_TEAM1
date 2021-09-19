from flask import jsonify, request, render_template, url_for, redirect
from mainapp import *
import time

@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
async def home():
    introStr = "This flask server for ICT3102: " + "\n" + "/add device : to add device"
    return introStr

@app.route('/list_device', methods=['GET'])
async def listDevice():
    return jsonify(deviceDic)

@app.route('/device_ping', methods=['POST'])
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
    insertLocation(tmpDic, cur, staff_id)
    if staff_id in deviceDic.keys():
        deviceDic[staff_id].append(tmpDic)
        return "Device updated."
    else:
        deviceDic[staff_id] = [tmpDic]
        return "Device added."

@app.route('/extractbeacon', methods=['GET'])
async def extractbeacon():
    staff_id = request.args.get('staff_id', type = int)
    start_time = request.args.get('start_time', type = int)
    end_time = request.args.get('end_time', type = int)
    
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT * FROM location WHERE staff_id = ? AND timestamp>? AND timestamp < ? ", (staff_id, start_time, end_time, ))
    location = cur.fetchall()
    return jsonify(location)


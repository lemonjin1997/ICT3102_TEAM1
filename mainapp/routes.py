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

@application.route("/register", methods=['POST'])
async def post():
    staff_username = request.json['staff_username']
    staff_password = request.json['staff_password']
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE username=?", (staff_username, ))
    cur.fetchall()
    if cur.rowcount > 0:
        errorStr = "Sorry username taken!"
        print(errorStr)
        return errorStr
    else:
        cur.execute("INSERT INTO staff(username, password) VALUES (?,?)", (staff_username, staff_password, ))
        con.commit()
        message = "Registered " + staff_username
        return message
    

@application.route('/login', methods=['POST'])
async def login():
    staff_username = request.json['staff_username']
    staff_password = request.json['staff_password']
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE username=? AND password=?", (staff_username, staff_password, ))
    staff_id = cur.fetchall()
    if staff_id.count() > 0:
        message = {"Message": "Login Successfully!", "staff_id": staff_id[0]}
        print(message)
        return message
    else:
        message = {"Message": "Login Failed!"}
        print(message)
        return message
    
    

@application.route('/temp_route', methods=['POST'])
def temp_route():
    staff_id = request.json['staff_id']
    beacon_mac = request.json['mac']
    print('Successfully received payload (ID:{staff_id} MAC:{beacon_mac})')
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE staff_id=?", (staff_id, ))
    staff_id = cur.fetchall()
    print(staff_id)
    if len(staff_id) > 0:
        cur.execute('INSERT INTO record(staff_id, beacon_mac, timestamp) VALUES (?,?,?)', (int(staff_id[0][0]), beacon_mac, int(time.time()),  ))
        return {'response' : f'Successfully received payload (ID:{staff_id} MAC:{beacon_mac})'}
    else:
        return {'response': 'Staff_id error'}
    


@application.route('/extractbeacon', methods=['GET'])
async def extractbeacon():
    staff_id = request.args.get('staff_id', type = int)
    start_time = request.args.get('start_time', type = int)
    end_time = request.args.get('end_time', type = int)
    
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("SELECT * FROM record WHERE staff_id = ? AND timestamp>? AND timestamp < ? ", (staff_id, start_time, end_time, ))
    location = cur.fetchall()
    print(location)
    return jsonify(location)


import flask
from flask import jsonify
from flask import request
import time
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

deviceDic = {}

pingInterval = 10

def connectionToDB():
    con = sqlite3.connect('ICT3102.db')
    return con

def startup():
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS staff (
        staff_id INTEGER PRIMARY KEY
    )
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS location (
        level INTEGER NOT NULL,
        location TEXT PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        staff_id INTEGER NOT NULL, 
        FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
        )
    """)
    return con

con = startup()

staff_id = 1

#introStr not read from file to reduce overhead
#async to allow threading
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

async def insertLocation(tmpDic, cur, staff_id):
    cur.execute("INSERT INTO location(level, location, timestamp, staff_id) VALUES (?,?,?,?)", (tmpDic['level'],tmpDic['location'],tmpDic['timestamp'],staff_id, ))
    con.commit()
    print("Insert location for " + staff_id)

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
    #start_time = time.localtime(start_time)
    #print(str(start_time.tm_hour) + ":" + str(start_time.tm_min) + ":" + str(start_time.tm_sec))

# maintaining dictionary/device list at an interval of 10 mins
def maintainingDic():
    for key in deviceDic.keys():
        if deviceDic[key]["timestamp"] + 1800 < time.time():
            deviceDic.pop(key)
    print("maintaining update")


    


sched_0 = BackgroundScheduler(daemon=True)
sched_0.add_job(maintainingDic,'interval',seconds=600)
sched_0.start()
app.run()
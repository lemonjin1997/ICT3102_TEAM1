from flask import Flask
import sqlite3
import time

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

# maintaining dictionary/device list at an interval of 10 mins
def maintainingDic():
    for key in deviceDic.keys():
        if deviceDic[key]["timestamp"] + 1800 < time.time():
            deviceDic.pop(key)
    print("maintaining update")


async def insertLocation(tmpDic, cur, staff_id):
    cur.execute("INSERT INTO location(level, location, timestamp, staff_id) VALUES (?,?,?,?)", (tmpDic['level'],tmpDic['location'],tmpDic['timestamp'],staff_id, ))
    con.commit()
    print("Insert location for " + staff_id)

app = Flask(__name__)
app.config["DEBUG"] = True

con = startup()

deviceDic = {}
pingInterval = 10

from mainapp import routes

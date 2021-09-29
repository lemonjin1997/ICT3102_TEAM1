from flask import Flask
import sqlite3



def connectionToDB():
    con = sqlite3.connect('ICT3102.db')
    return con

def startup():
    con = connectionToDB()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS staff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username char(8),
        password char(8)
    )
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS record (
        record INTEGER PRIMARY KEY AUTOINCREMENT,
        beacon_mac char(20),
        timestamp INTEGER NOT NULL,
        staff_id INTEGER NOT NULL, 
        FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
        )
    """)
    cur.execute("INSERT INTO staff(username, password) VALUES('username1', 'password1')")
    con.commit()
    
    return con

application = Flask(__name__)
application.config["DEBUG"] = True

con = startup()

deviceDic = {}
pingInterval = 10

from mainapp import routes
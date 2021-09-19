from flask import Flask
import sqlite3

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

app = Flask(__name__)
app.config["DEBUG"] = True

con = startup()

deviceDic = {}
pingInterval = 10

from mainapp import routes

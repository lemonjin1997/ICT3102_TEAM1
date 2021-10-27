import sqlite3
import time

locationDic = {"F43EC609E95" : {"level": 1, "location": "location1"} ,"FE1C328D7D15" : {"level": 2, "location": "location2"} }




def insertUser(con, staff_username, staff_password):
    cur = con.cursor()
    cur.execute("INSERT INTO staff(username, password) VALUES (?,?)", (staff_username, staff_password, ))
    con.commit()
    print("Insert staff!")

def getUsername(con, staff_username):
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE username=?", (staff_username, ))
    return cur.fetchall()

def userLogin(con, staff_username, staff_password):
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE username=? AND password=?", (staff_username, staff_password, ))
    staff_id = cur.fetchall()
    return staff_id

def staffIdCheck(con, staff_id):
    cur = con.cursor()
    cur.execute("SELECT staff_id FROM staff WHERE staff_id=?", (staff_id, ))
    staff_id = cur.fetchall()
    print(staff_id)
    return len(staff_id) > 0

def extractBeaconData(con, staff_id, start_time, end_time):
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM record")# WHERE staff_id = ? AND timestamp>? AND timestamp < ? ", (staff_id, start_time, end_time, ))
    locations = cur.fetchall()
    print(locationDic)
    for location in locations:
        del location["staff_id"]
        del location["record"]
        location['level'] = locationDic[location['beacon_mac']]['level']
        location['location'] = locationDic[location['beacon_mac']]['location']
        del location["beacon_mac"]
    return locations

def insertPing(con, staff_id, beacon_mac):
    cur = con.cursor()
    cur.execute('INSERT INTO record(staff_id, beacon_mac, timestamp) VALUES (?,?,?)', (int(staff_id[0][0]), beacon_mac, int(time.time()),  ))
    con.commit()

#https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
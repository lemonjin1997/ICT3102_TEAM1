import time

def maintainingDic(dic):
    for key in dic.keys():
        if dic[key]["timestamp"] + 1800 < time.time():
            dic.pop(key)
    print("maintaining update")

async def insertLocation(con, tmpDic, staff_id):
    con.cursor().execute("INSERT INTO location(level, location, timestamp, staff_id) VALUES (?,?,?,?)", (tmpDic['level'],tmpDic['location'],tmpDic['timestamp'],staff_id, ))
    con.commit()
    print("Insert location for " + staff_id)

def insertUser():
    pass
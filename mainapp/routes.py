from flask import jsonify, request, render_template, url_for, redirect
from mainapp import application, connectionToDB
from mainapp.utilities import * 



@application.route('/', methods=['GET'])
@application.route('/home/', methods=['GET'])
def home():
    introStr = "This flask server for ICT3102: " + "\n" 
    return introStr


@application.route("/register", methods=['POST'])
async def post():
    staff_username = request.json['staff_username']
    staff_password = request.json['staff_password']
    con = connectionToDB()
    userName = getUsername(con, staff_username)

    if len(userName) > 0:
        errorStr = "Sorry username taken!"
        print(errorStr)
        return errorStr
    else:
        insertUser(con, staff_username, staff_password)
        message = "Registered " + staff_username
        return message
    

@application.route('/login', methods=['POST'])
async def login():
    staff_username = request.json['staff_username']
    staff_password = request.json['staff_password']
    con = connectionToDB()
    staff_id = userLogin(con, staff_username, staff_password)
    if len(staff_id) > 0:
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
    if staffIdCheck(con, staff_id):
        insertPing(con, staff_id, beacon_mac)
        return {'response' : f'Successfully received payload (ID:{staff_id} MAC:{beacon_mac})'}
    else:
        return {'response': 'Staff_id error'}
    


@application.route('/extractbeacon', methods=['GET'])
async def extractbeacon():
    staff_id = request.args.get('staff_id', type = int)
    start_time = request.args.get('start_time', type = int)
    end_time = request.args.get('end_time', type = int)
    
    con = connectionToDB()
    data = extractBeaconData(con, staff_id, start_time, end_time)
    data = {"locations" : data}
    print(data)

    return data



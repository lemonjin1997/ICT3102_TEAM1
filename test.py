from timeit import timeit
from mainapp.routes import * 
import requests

url = "http://127.0.0.1:5000/"


def TempRouteTest():
    responseTempRoute = requests.post(url + "temp_route", json={"staff_id" : "1", "mac" : "mac_address"})
    if responseTempRoute.status_code == 200:
        print("temproute success")

def ExtractBeaconTest():
    responseExtractBeacon = requests.get(url + "extractbeacon"+ "?staff_id=1&start_time=1630559263&end_time=1630559273")
    if responseExtractBeacon.status_code == 200:
        print("extractbeacon succcess")

print(timeit("TempRouteTest()", 'from __main__ import TempRouteTest', number=1))
print(timeit("ExtractBeaconTest()", 'from __main__ import ExtractBeaconTest', number=1))

print(timeit("insertPing(con, staff_id, beacon_mac)", 'from mainapp.utilities import insertPing; from mainapp.__init__ import connectionToDB; staff_id = "1"; beacon_mac = "beaonc1"; con = connectionToDB();', number=1))

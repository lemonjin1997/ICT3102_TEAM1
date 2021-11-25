from pydantic import BaseModel

class User(BaseModel):
    name:str

class Beacon(BaseModel):
    beacon_mac: str
    location: str
    level: str

class Ping(BaseModel):
    time_stamp: str
    beacon_mac: str
    name: str
    RSSI:str
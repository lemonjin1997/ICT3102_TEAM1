def UserEntity(item) -> dict:
    return {
        "id": str(item(["_id"])),
        "name": item(["name"]),
        "email": item(["email"]),
        "password": item(["password"])
    }

def UsersEntity(entity) -> list:
    return [UserEntity(item) for item in entity]


def BeaconEntity(item) -> dict:
    return {
        "id": str(item(["_id"])),
        "beacon_mac": item(["beacon_mac"]),
        "location": item(["location"]),
        "level": item(["level"])
    }

def BeaconsEntity(entity) -> list:
    return [BeaconEntity(item) for item in entity]

def PingEntity(item) -> list:
    return {
        "id": str(item(["_id"])),
        "beacon_mac" : item(["beacon_mac"]),
        "time_stamp" : item(["time_stamp"]),
        "name" : item(["name"])
    }

def PingsEntity(entity) -> dict:
    return [PingEntity(item) for item in entity]
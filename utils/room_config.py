import random

def generate_room_code():
    code = str(random.randint(1000, 9999))
    room_code = "LAMP-" + code
    return room_code

def generate_room_name():
    names = ["Lighthouse", "Beacon", "Bonfire", "Campfire"]
    room_name = random.choice(names)
    return room_name

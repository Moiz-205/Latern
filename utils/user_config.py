import os
import json
import random


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "user_config.json")

def default_config_generator():
    names = ["firefly", "cat", "dog"]
    colors = ["red", "green", "blue"]
    default_name = random.choice(names)
    default_color = random.choice(colors)
    return default_name, default_color

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            username = data.get("username")
            usercolor = data.get("color")
            return username, usercolor
    else:
        username, usercolor = default_config_generator()
        with open(CONFIG_PATH, "w") as f:
            json.dump({"username": username, "color": usercolor}, f)
            return username, usercolor

def update_config(username, usercolor):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"username": username, "color": usercolor}, f)

import json
from pathlib import Path
import datetime

user_file_path = Path(__file__).parent.parent / "data" / "Users.json"
settings_file_path = Path(__file__).parent.parent / "data" / "settings.json"

with settings_file_path.open("r") as f:
    settings = json.load(f)

with user_file_path.open("r") as f:
    user_data = json.load(f)

def save_data():
    with user_file_path.open("w") as f:
        json.dump(user_data, f, indent=4)

def agregar_usuario(user):
    user_template = {
        "piezas": {},
        "sesiones": {}
    }
    user_data[user.username] = user_template
    save_data()

def record(user, pieza, time):
    if pieza not in user.data["piezas"]:
        print("Error: pieza no encontrada!")
        return
    
    user.data["piezas"][pieza] += time
    date = str(datetime.date.today())
    if not date in user.data["sesiones"]:
        user.data["sesiones"][date] = []
    user.data["sesiones"][date].append([pieza, time])

    save_data()
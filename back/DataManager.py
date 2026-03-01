import json
from pathlib import Path
import datetime

user_file_path = Path(__file__).parent.parent / "data" / "Users.json"
settings_file_path = Path(__file__).parent.parent / "data" / "settings.json"

def load_json(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with path.open("w") as f:
            json.dump({}, f, indent=4)
        return {}

settings = load_json(settings_file_path)
user_data = load_json(user_file_path)

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
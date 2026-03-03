import json
from pathlib import Path
import datetime
import re

# Load data files
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

def dump_compact_lists(data, file):
    text = json.dumps(data, indent=2)

    pattern = r'\[\s+([^\[\]\{\}]+?)\s+\]'
    while re.search(pattern, text):
        text = re.sub(
            pattern,
            lambda m: "[" + " ".join(m.group(1).split()) + "]",
            text
        )

    file.write(text)

# Data Management

def raw_save():

    with user_file_path.open("w") as f:
        dump_compact_lists(user_data, f) # compact
        # json.dump(user_data, f, indent=4) ugly

def agregar_usuario(user):

    user_template = {
        "piezas": {},
        "sesiones": []
    }
    user_data[user.username] = user_template

    raw_save()

# Getters

def get_piece_id(user, piece) -> str | None:

    for id, item in user.data['piezas'].items():
        if item[0] == piece: return id
    return None

def is_piece_active(user, id: str) -> bool:

    if id in user.data['piezas']:
        return user.data['piezas'][id][1]
    else:
        return False

def get_actives(user) -> list:
    actives = []

    for item in user.data['piezas'].values():
        if item[1]: actives.append(item[0])
    
    return actives

def get_displayable_session(user, session: list) -> tuple:

    date, id, t = session
    
    # DATE
    _, month, day = date.split('-')
    out_date = f'{day}/{month}'

    # PIECE
    piece_name = user.data['piezas'][id][0]

    # TIME
    m = (t % 3600) // 60
    h = t // 3600

    if h != 0 and m != 0:
        out_time = f'{h}h {m} min'
    elif h == 0 and m == 0:
        out_time = f'{t % 60} seg'
    elif h == 0:
        out_time = f'{m} min'
    else:
        out_time = f'{h}h'

    return (out_date, piece_name, out_time)

def get_session_month(session: list) -> int:
    
    _, month, _ = session[0].split('-')
    return int(month)

# Setters

def record(user, id: str, time: int) -> None:

    if id not in user.data["piezas"]:
        print("Error: pieza no encontrada!")
        return
    
    date = str(datetime.date.today())
    user.data["sesiones"].append([date, id, time])
    raw_save()

def create_piece(user, piece: str) -> None:
    if piece == "" or len(piece) > 25: return

    # Activate piece (if it's there)
    for item in user.data['piezas'].values():
        if piece != item[0]: continue
        item[1] = True
        raw_save()
        return
    
    # Create piece (if it's not there)
    new_index = len(user.data['piezas']) + 1
    user.data['piezas'][str(new_index)] = [piece, True]

    raw_save()

def erase_piece(user, piece: str) -> None:

    for _, item in user.data['piezas'].items():
        if piece != item[0]: continue
        item[1] = False
        return
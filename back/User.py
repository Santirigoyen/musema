import back.DataManager as dm

class User():
    def __init__(self, username):
        self.username = username
        if not username in dm.user_data:
            dm.agregar_usuario(self)
        self.data = dm.user_data[username]
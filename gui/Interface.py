from back.DataManager import *
from back.User import User
from customtkinter import *
from gui.StatsGui import StatsFrame
from gui.SessionGui import SessionFrame, TimerFrame
from gui.PiecesGui import PieceFrame
from PIL import Image
import gui.GuiTemplates as gui

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']

IMGs = {
    'play': Image.open(settings['images']['play']),
    'piano': Image.open(settings['images']['piano']),
    'stats': Image.open(settings['images']['stats']),
}
on_session = False

# Menu Frame

class Sidebar(CTkFrame):
    def __init__(self, parent, p_menu):
        super().__init__(parent, fg_color=COLORS['dark'], border_width=0)

        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1)


        # Menu Buttons
        self.options = [
            gui.MenuButton(self, 0, 'Sesión', IMGs['play'], lambda: self.change_menu(0, p_menu)),
            gui.MenuButton(self, 1, 'Piezas', IMGs['piano'], lambda: self.change_menu(1, p_menu)),
            gui.MenuButton(self, 2, 'Estadísticas', IMGs['stats'], lambda: self.change_menu(2, p_menu))
        ]
        self.options[0].configure(fg_color=COLORS['bg'])
    
    def change_menu(self, index, p_menu):
        global on_session
        if on_session: return
        p_menu(index)
        for button in self.options:
            button.configure(fg_color=COLORS['dark'])
        self.options[index].configure(fg_color=COLORS['bg'])

# Main stuff

class MainFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['dark'], border_width=0)

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2,3,4), weight=1, uniform='a')

        # Menu frames
        self.sidebar = Sidebar(self, self.menu)
        self.sidebar.grid(column=0,sticky='nsew',pady=5)

        self.user: User

    def setup(self, user):
        self.user = user

        # Create menus
        self.menu_frames = [
            SessionFrame(self),
            PieceFrame(self),
            StatsFrame(self),
            TimerFrame(self)
        ]
        for mf in self.menu_frames:
            mf.grid(column=1,row=0,columnspan=4,sticky='nsew')

        self.current = -1

        # Set to initial menu        
        if len(self.user.data['piezas']) == 0:
            self.sidebar.change_menu(1, self.menu)
        else:
            self.sidebar.change_menu(0, self.menu)

    def menu(self, i):
        if self.current == i: return
        self.current = i
        self.focus()
        current = self.menu_frames[i]
        current.tkraise()
        if i == 0: current.update_options()
    
    def start_session(self, piece):
        if self.user == None: return
        timer_f = self.menu_frames[3]

        timer_f.choice.set(piece)
        timer_f.initimer(piece)
        timer_f.update_recorded()
        self.menu(3)


class LoginFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0)

        self.app = parent

        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        gui.TitleLabel(self, 'Login').grid(row=2)

        self.textbox = gui.EntryBox(self, 'Username')
        self.textbox.grid(row=3, sticky='ew', padx=95, pady=25)
        
        self.username = ''
        self.textbox.bind("<Return>", self.check_input)
    
    # Detect Enter
    def check_input(self, e):
        name = self.textbox.get()
        if name == '': return
        self.app.focus()
        self.app.user = User(name)
        self.app.access()


class App(CTk):
    def __init__(self):
        super().__init__()

        self.window_config()
        self.create_frames()

        self.user = None

        self.login_setup()
        self.login.tkraise()

    def window_config(self):

        self.title('Musema')
        self.iconbitmap(default=settings['images']['icon'])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure(fg_color=COLORS['bg'])

    def create_frames(self):

        self.login = LoginFrame(self)
        self.main = MainFrame(self)
        self.login.grid(row=0,column=0,sticky="nsew")
        self.main.grid(row=0,column=0,sticky="nsew")
    
    def access(self):

        offset_x = (settings['app_size'][0] - 500) // 2
        offset_y = (settings['app_size'][1] - 400) // 2

        self.geometry(
            f'{settings['app_size'][0]}x{settings['app_size'][1]}' + # Size
            f'+{self.winfo_x() - offset_x}+{self.winfo_y() - offset_y}') # Pos
            
        self.resizable(False, False)
        self.main.setup(self.user)
        self.main.tkraise()
    
    def login_setup(self):

        self.geometry('500x400')
        self.resizable(False, False)


def display():
    app = App()
    app.mainloop()
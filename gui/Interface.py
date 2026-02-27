from back.DataManager import *
from back.User import User
from customtkinter import *
from tkinter import PhotoImage
from gui.StatsGui import StatsFrame
from gui.SessionGui import SessionFrame, TimerFrame
from gui.PiecesGui import PieceFrame
from PIL import Image

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
            MenuButton(self, 0, 'Sesión', IMGs['play'], lambda: self.change_menu(0, p_menu)),
            MenuButton(self, 1, 'Piezas', IMGs['piano'], lambda: self.change_menu(1, p_menu)),
            MenuButton(self, 2, 'Estadísticas', IMGs['stats'], lambda: self.change_menu(2, p_menu))
        ]
        self.options[0].configure(fg_color=COLORS['bg'])
    
    def change_menu(self, index, p_menu):
        global on_session
        if on_session: return
        p_menu(index)
        for button in self.options:
            button.configure(fg_color=COLORS['dark'])
        self.options[index].configure(fg_color=COLORS['bg'])

class MenuButton(CTkButton):
    def __init__(self, parent, row, text, img, cmd):
        super().__init__(parent,
            fg_color=COLORS['dark'],
            text=text,
            text_color=COLORS['text'],
            font=(FONT, FONTS['small']),
            image=CTkImage(img),
            compound='left',
            anchor='w',
            border_spacing=6,
            corner_radius=8,
            command=cmd,
            hover_color=COLORS['mid'])

        self.grid(row=row, padx=6, pady=3, sticky='nsew')

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

    def menu(self, i):
        if self.current == i: return
        self.current = i
        self.focus()
        current = self.menu_frames[i]
        current.tkraise()
        if i == 0: current.update_options()
    
    def start_session(self, piece):
        if self.user == None: return
        self.menu_frames[3].choice.set(piece)
        self.menu_frames[3].initimer(piece)
        self.menu_frames[3].update_recorded()
        self.menu(3)

    def setup(self, user):
        self.user = user
        self.menu_frames = [
            SessionFrame(self),
            PieceFrame(self),
            StatsFrame(self),
            TimerFrame(self)
        ]
        for mf in self.menu_frames:
            mf.grid(column=1,row=0,columnspan=4,sticky='nsew')

        self.current = -1
        
        if len(self.user.data['piezas']) == 0:
            self.sidebar.change_menu(1, self.menu)
        else:
            self.sidebar.change_menu(0, self.menu)


class LoginFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0)

        self.app = parent

        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Login Title
        CTkLabel(self,
            text='Login',
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg']
        ).grid(row=2)

        # Username Textbox
        self.textbox = CTkEntry(self,
            font=(FONT,
            FONTS['normal']),
            fg_color=COLORS['dark'],
            border_width=0,
            text_color=COLORS['text'],
            placeholder_text='Username')
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

        # Window CONFIG
        self.title('Musema')
        self.iconbitmap(default=settings['images']['icon'])
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color=COLORS['bg'])

        # Main Frames
        self.login = LoginFrame(self)
        self.main = MainFrame(self)
        self.login.grid(row=0,column=0,sticky="nsew")
        self.main.grid(row=0,column=0,sticky="nsew")

        self.user = None

        self.login_setup()
        self.login.tkraise()
    
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
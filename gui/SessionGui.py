from customtkinter import *
from back.DataManager import *
from back.SessionTimer import Timer
import gui.GuiTemplates as gui
from PIL import Image

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']
IMGs = {
    'play': Image.open(settings['images']['play']),
    'finish': Image.open(settings['images']['finish']),
    'pause': Image.open(settings['images']['pause']),
    'back': Image.open(settings['images']['back'])
}

class SessionFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0, corner_radius=0)

        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.parent = parent
        self.user = parent.user

        self.setup_labels()
    
    def setup_labels(self):

        # Title
        gui.TitleLabel(self, 'Sesión').grid(row=1, sticky='w', padx=90)

        # Dropdown
        pieces = list(self.user.data['piezas'])

        self.choice = gui.Dropdown(self, 380, 55,
            pieces, len(pieces) == 0)
        self.choice.grid(row=2, sticky='w', padx=80)

        # → Button
        self.next = gui.SpecialLabButton(self, '→', self.start_session)
        self.next.grid(row=2, sticky='e', padx=80)

    def start_session(self):
        if len(self.user.data['piezas']) > 0:
            self.parent.start_session(self.choice.get())

    def update_options(self):
        self.choice.configure(values=['...'] if len(self.user.data['piezas'])==0 else list(self.user.data['piezas']))
        if len(self.user.data['piezas']) > 0:
            self.choice.set(list(self.user.data['piezas'].keys())[0])
        else: self.choice.set('...')

class TimerFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=COLORS['bg'], border_width=0, corner_radius=0)
        self.parent = parent
        self.user = parent.user
        self.timer: Timer

        self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1)

        self.setup_labels()
    
    def setup_labels(self):

        # Title
        self.choice = StringVar()

        gui.TitleVar(self, self.choice).grid(row=1, sticky='we')

        # Clock BG
        gui.DarkFrame(self).grid(row=2, rowspan=2, padx=120, pady=20, sticky='nsew')

        # Clock Label
        self.number = StringVar(value='00:00:00')
        self.milinum = StringVar(value='.00')

        gui.BaseVarLabel(self, self.number, FONTS['title'] * 1.475
        ).grid(row=2, rowspan=2, padx=170, pady=20, sticky='w')

        gui.BaseVarLabel(self, self.milinum
        ).grid(row=2, rowspan=2, padx=170, pady=38, sticky='se')

        # Recorded Label
        self.recorded_lab = gui.BaseLabel(self, 'Sesión guardada exitósamente!', (FONT, FONTS['normal'], 'bold'))

        # Back
        gui.IconButton(self, 'back', self.back, COLORS['bg'], 0, 70).grid(row=0,sticky='w')

        # Confirm cancel
        self.cancel_confirm = gui.BaseLabel(self, 'Cancelar sesión?', (FONT, FONTS['normal'], 'bold'))
        self.cancel_confirm.grid(row=0,sticky='w',padx=80)

        # Play
        self.play_b = gui.SpecialImgButton(self, 'play', self.play_timer, 0, 100, 50)
        self.play_b.grid(row=4, padx=170, sticky='w')

        # Pause
        self.pause_b = gui.SpecialImgButton(self, 'pause', self.pause_timer, 0, 100, 50, COLORS['light'], COLORS['bg'])
        self.pause_b.grid(row=4, padx=170, sticky='e')

    def pause_timer(self):
        if self.timer.paused: # unpause

            self.pause_b.configure(image=CTkImage(IMGs['pause']))
        elif self.timer.running: # pause

            self.pause_b.configure(image=CTkImage(IMGs['play']))

        self.timer.pause()

    def play_timer(self):
        if self.timer.running or self.timer.paused: # reset

            self.recorded_lab.grid(row=6, sticky='new')
            self.play_b.configure(image=CTkImage(IMGs['play']), fg_color=COLORS['green'], hover_color=COLORS['light-green'])
            self.pause_b.configure(image=CTkImage(IMGs['pause']))
            self.cancel_confirm.configure(text_color=COLORS['bg'])

        elif not self.timer.paused: # play

            self.recorded_lab.grid_forget()
            self.play_b.configure(image=CTkImage(IMGs['finish']), fg_color=COLORS['red'], hover_color=COLORS['light-red'])
        
        self.timer.play()
    
    def update_clock(self, h, m, s, ms):
        self.number.set(f'{h:02}:{m:02}:{s:02}')
        self.milinum.set(f'.{ms:02}')
            
    def back(self):
        if self.cancel_confirm.cget("text_color") == COLORS['bg'] and (self.timer.running or self.timer.paused): # Show pop-up
            self.cancel_confirm.configure(text_color=COLORS['light'])

            self.after(3000, lambda: self.cancel_confirm.configure(text_color=COLORS['bg']) if self.cancel_confirm.cget("text_color") == COLORS['light'] else None) # Reset after 5s
        else: # Confirm
            self.timer.cancel()
            self.parent.menu(0)
    
    def initimer(self, piece):
        self.timer = Timer(self, self.user, piece)
    
    def update_state(self, value):
        global on_session
        on_session = value

    def update_recorded(self):
        self.recorded_lab.configure(text_color=COLORS['bg'])
        self.cancel_confirm.configure(text_color=COLORS['bg'])
        self.play_b.configure(image=CTkImage(IMGs['play']), fg_color=COLORS['green'], hover_color=COLORS['light-green'])
        self.pause_b.configure(image=CTkImage(IMGs['pause']))

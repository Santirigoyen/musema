from customtkinter import *
from back.DataManager import *
from back.SessionTimer import Timer
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

        # Title
        CTkLabel(self,
            text='Sesión',
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg']
        ).grid(row=1, sticky='w', padx=90)
        

        pieces = list(self.user.data['piezas'])
        # Dropdown
        self.choice = CTkOptionMenu(self,
            font=(FONT, FONTS['normal']),
            dropdown_font=(FONT, FONTS['normal']*0.75),
            dropdown_fg_color=COLORS['bg'],
            text_color=COLORS['text'],
            dropdown_text_color=COLORS['text'],
            fg_color=COLORS['dark'],
            button_color=COLORS['dark'],
            width=380,
            height=55,
            corner_radius=10,
            hover=False,
            dynamic_resizing=False,
            values= ['...'] if len(pieces) == 0 else pieces)
        
        self.choice.grid(row=2, sticky='w', padx=80)

        # → Button
        self.next = CTkButton(self,
            font=(FONT, FONTS['normal'], 'bold'),
            text='→',
            text_color=COLORS['text'],
            fg_color=COLORS['green'],
            hover_color=COLORS['light-green'],
            height=50,
            width=80,
            corner_radius=10,
            command=self.start_session)
        
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

        # Title
        self.choice = StringVar()

        CTkLabel(self,
            textvariable=self.choice,
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg']
        ).grid(row=1, sticky='we')

        # Clock BG
        CTkFrame(self,
            fg_color=COLORS['dark'],
            corner_radius=20
        ).grid(row=2, rowspan=2, padx=120, pady=20, sticky='nsew')

        # Clock Label
        self.number = StringVar(value='00:00:00')
        self.milinum = StringVar(value='.00')

        CTkLabel(self,
            textvariable=self.number,
            font=(FONT, FONTS['title'] * 1.475),
            text_color=COLORS['text'],
            fg_color=COLORS['dark'],
            corner_radius=0,
        ).grid(row=2, rowspan=2, padx=170, pady=20, sticky='w')

        CTkLabel(self,
            textvariable=self.milinum,
            font=(FONT, FONTS['title']),
            text_color=COLORS['text'],
            fg_color=COLORS['dark'],
            height=0,
            width=0
        ).grid(row=2, rowspan=2, padx=170, pady=38, sticky='se')

        # Recorded Label
        self.recorded_lab = CTkLabel(self,
            text='Sesión guardada exitósamente!',
            font=(FONT, FONTS['normal'], 'bold'),
            fg_color=COLORS['bg'],
            text_color=COLORS['bg'])
        self.recorded_lab.grid(row=6, sticky='new')

        # Back
        CTkButton(self,
            image=CTkImage(IMGs['back']),
            fg_color=COLORS['bg'],
            anchor='w',
            corner_radius=35,
            width=0,
            height=70,
            text='',
            hover=False,
            command=self.back
        ).grid(row=0,sticky='w')

        # Confirm cancel
        self.cancel_confirm = CTkLabel(self,
            text='Cancelar sesión?',
            font=(FONT, FONTS['normal'], 'bold'),
            fg_color=COLORS['bg'],
            text_color=COLORS['bg'])
        self.cancel_confirm.grid(row=0,sticky='w',padx=80)

        # Play
        self.play_b = CTkButton(self,
            image=CTkImage(IMGs['play']),
            fg_color=COLORS['green'],
            anchor='w',
            corner_radius=50,
            width=0,
            height=100,
            text='',
            hover_color=COLORS['light-green'],
            command=self.play_timer)
        self.play_b.grid(row=4, padx=170, sticky='w')

        # Pause
        self.pause_b = CTkButton(self,
            image=CTkImage(IMGs['pause']),
            fg_color=COLORS['light'],
            corner_radius=50,
            width=0,
            height=100,
            text='',
            hover_color=COLORS['bg'],
            command=self.pause_timer)
        self.pause_b.grid(row=4, padx=170, sticky='e')

    def pause_timer(self):
        if self.timer.paused: # unpause

            self.pause_b.configure(image=CTkImage(IMGs['pause']))
        elif self.timer.running: # pause

            self.pause_b.configure(image=CTkImage(IMGs['play']))

        self.timer.pause()

    def play_timer(self):
        if self.timer.running or self.timer.paused: # reset

            self.recorded_lab.configure(text_color=COLORS['light'])
            self.play_b.configure(image=CTkImage(IMGs['play']), fg_color=COLORS['green'], hover_color=COLORS['light-green'])
            self.pause_b.configure(image=CTkImage(IMGs['pause']))
            self.cancel_confirm.configure(text_color=COLORS['bg'])

        elif not self.timer.paused: # play

            self.recorded_lab.configure(text_color=COLORS['bg'])
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

from back.DataManager import *
from customtkinter import *
from PIL import Image

COLORS = settings['colors']
FONTS = settings['fontsizes']
FONT = settings['font']

IMGs = {
    'trash': Image.open(settings['images']['trash']),
    'plus': Image.open(settings['images']['plus']),
    'play': Image.open(settings['images']['play']),
    'pause': Image.open(settings['images']['pause']),
    'back': Image.open(settings['images']['back']),
    'reload': Image.open(settings['images']['reload']),
    'export': Image.open(settings['images']['export']),
    'right_arrow': Image.open(settings['images']['right_arrow']),
    'left_arrow': Image.open(settings['images']['left_arrow'])
}

class BaseLabel(CTkLabel):
    def __init__(self, parent, text, font=(FONT, FONTS['normal']), fg_color=COLORS['bg']):
        super().__init__(parent,
            text=text,
            font=font,
            text_color=COLORS['text'],
            fg_color=fg_color)

class BaseVarLabel(CTkLabel):
    def __init__(self, parent, text_var, size=FONTS['title'], fg=COLORS['dark']):
        super().__init__(parent,
            textvariable=text_var,
            font=(FONT, size),
            text_color=COLORS['text'],
            fg_color=fg,
            corner_radius=0)

class SpecialLabButton(CTkButton):
    def __init__(self, parent, text, command, width=80, height=50):
        super().__init__(parent,
        font=(FONT, FONTS['normal'], 'bold'),
        text=text,
        text_color=COLORS['text'],
        fg_color=COLORS['green'],
        hover_color=COLORS['light-green'],
        height=height,
        width=width,
        corner_radius=10,
        command=command)

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

class TitleLabel(CTkLabel):
    def __init__(self, parent, text):
        super().__init__(parent,
            text=text,
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg'])

class TitleVar(CTkLabel):
    def __init__(self, parent, text_var):
        super().__init__(parent,
            textvariable=text_var,
            font=(FONT, FONTS['title'], 'bold'),
            text_color=COLORS['text'],
            fg_color=COLORS['bg'])

class EntryBox(CTkEntry):
    def __init__(self, parent, placeholder, width=140):
        super().__init__(parent,
            font=(FONT, FONTS['normal']),
            fg_color=COLORS['dark'],
            text_color=COLORS['text'],
            placeholder_text=placeholder,
            width=width)

class WarningLabel(CTkLabel):
    def __init__(self, parent, text, font, fg_color=COLORS['dark']):
        super().__init__(parent,
            text=text,
            font=font,
            fg_color=fg_color,
            text_color=COLORS['light-red'])
        
class IconButton(CTkButton):
    def __init__(self, parent, img, command, fg=COLORS['dark'], width=40, height=40):
        super().__init__(parent,
            text='',
            image=CTkImage(IMGs[img]),
            width=width,
            height=height,
            corner_radius=10,
            fg_color=fg,
            hover_color=COLORS['bg'],
            command=command)
        
class SpecialImgButton(CTkButton):
    def __init__(self, parent, img, command, width=80, height=28, radius=10, fg=COLORS['green'], hover=COLORS['light-green']):
        super().__init__(parent,
            text='',
            text_color=COLORS['text'],
            image=CTkImage(IMGs[img]),
            width=width,
            height=height,
            corner_radius=radius,
            fg_color=fg,
            hover_color=hover,
            command=command)
        
class PieceCheckbox(CTkCheckBox):
    def __init__(self, parent, command):
        super().__init__(parent,
            border_color=COLORS['darker'],
            fg_color=COLORS['bg'],
            checkmark_color=COLORS['text'],
            hover=False,
            text='',
            width=0,
            command=command)
        
class Dropdown(CTkOptionMenu):
    def __init__(self, parent, width, height, values, empty_condition):
        super().__init__(parent,
            font=(FONT, FONTS['normal']),
            dropdown_font=(FONT, FONTS['normal']*0.75),
            dropdown_fg_color=COLORS['bg'],
            text_color=COLORS['text'],
            dropdown_text_color=COLORS['text'],
            fg_color=COLORS['dark'],
            button_color=COLORS['dark'],
            corner_radius=10,
            hover=False,
            dynamic_resizing=False,
            width=width,
            height=height,
            values = ['...'] if empty_condition else values)

class DarkFrame(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,
            fg_color=COLORS['dark'],
            corner_radius=20)